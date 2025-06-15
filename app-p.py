import gradio as gr
import math
import pandas as pd
import io
from math import gcd
from functools import reduce

def find_gcd_multiple(*numbers):
    """Find GCD of multiple numbers"""
    return reduce(gcd, numbers)

def is_primitive_solution(a, b, c, d):
    """Check if solution is primitive (gcd = 1)"""
    return find_gcd_multiple(a, b, c, d) == 1

def get_primitive_form(a, b, c, d):
    """Convert solution to its primitive form"""
    common_factor = find_gcd_multiple(a, b, c, d)
    return (a//common_factor, b//common_factor, c//common_factor, d//common_factor, common_factor)

def create_results_dataframe(quadruplets):
    """Create pandas DataFrame from quadruplets for Excel export"""
    if not quadruplets:
        return pd.DataFrame()
    
    data = []
    for i, (a, b, c, d) in enumerate(quadruplets, 1):
        common_factor = find_gcd_multiple(a, b, c, d)
        is_primitive = common_factor == 1
        
        if is_primitive:
            primitive_form = f"({a}, {b}, {c}, {d})"
        else:
            prim_a, prim_b, prim_c, prim_d, _ = get_primitive_form(a, b, c, d)
            primitive_form = f"({prim_a}, {prim_b}, {prim_c}, {prim_d})"
        
        # Verification values
        left_side = d**3 - a**3
        right_side = b**3 + c**3
        
        data.append({
            'Solution_No': i,
            'a': a,
            'b': b, 
            'c': c,
            'd': d,
            'n': d - a,
            'Common_Factor': common_factor,
            'Type': 'Primitive' if is_primitive else 'Scaled',
            'Primitive_Form': primitive_form,
            'a³': a**3,
            'b³': b**3,
            'c³': c**3,
            'd³': d**3,
            'd³_minus_a³': left_side,
            'b³_plus_c³': right_side,
            'Equation_Check': 'Valid' if left_side == right_side else 'Invalid'
        })
    
    return pd.DataFrame(data)

def export_to_excel(quadruplets, filename="cube_quadruplets_results.xlsx"):
    """Export quadruplets to Excel file"""
    if not quadruplets:
        return None
    
    df = create_results_dataframe(quadruplets)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Main results sheet
        df.to_excel(writer, sheet_name='Quadruplets_Results', index=False)
        
        # Summary sheet
        summary_data = {
            'Metric': [
                'Total Solutions Found',
                'Primitive Solutions',
                'Scaled Solutions', 
                'Unique Common Factors',
                'Average a value',
                'Average d value',
                'Min quadruplet',
                'Max quadruplet'
            ],
            'Value': [
                len(quadruplets),
                len([q for q in quadruplets if is_primitive_solution(*q)]),
                len([q for q in quadruplets if not is_primitive_solution(*q)]),
                len(set(find_gcd_multiple(*q) for q in quadruplets)),
                f"{sum(q[0] for q in quadruplets) / len(quadruplets):.1f}",
                f"{sum(q[3] for q in quadruplets) / len(quadruplets):.1f}",
                str(min(quadruplets)),
                str(max(quadruplets))
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    return output.getvalue()

def find_cube_quadruplets_with_factors(a, n, max_iterations=10000, include_factors=True, max_factor=5):
    """
    ENHANCED: Find cube quadruplets with common factor analysis
    """
    try:
        a, n = int(a), int(n)
        max_iterations = int(max_iterations) if max_iterations > 0 else 10000
        max_factor = int(max_factor) if max_factor > 0 else 5
    except (ValueError, TypeError):
        return "Error: Please enter valid integers", []
    
    if a <= 0 or n <= 0:
        return "Error: Both 'a' and 'n' must be positive integers", []
    
    d = a + n
    target_sum = d**3 - a**3
    
    result_text = f"""🔍 **ENHANCED SEARCH WITH COMMON FACTORS:**
📊 **Parameters:**
• a = {a}, n = {n}, d = a + n = {d}
• Target: d³ - a³ = {target_sum:,}
• Include factor analysis: {'Yes' if include_factors else 'No'}
• Max factor to check: {max_factor if include_factors else 'N/A'}
{'='*70}
"""
    
    quadruplets = []
    primitive_solutions = []
    factor_families = {}
    search_details = ""
    iterations = 0
    
    # Search for solutions
    max_b = a - 1
    
    for b in range(max_b, 0, -1):
        iterations += 1
        
        if iterations % 1000 == 0:
            search_details += f"🔄 Searched {iterations} iterations... (current b = {b})\n"
        
        if iterations > max_iterations:
            search_details += f"⚠️ **Search stopped after {max_iterations:,} iterations**\n"
            break
        
        if b >= a or b >= d:
            continue
            
        b_cubed = b**3
        c_cubed_needed = target_sum - b_cubed
        
        if c_cubed_needed <= 0:
            continue
            
        c_exact = c_cubed_needed**(1/3)
        c = round(c_exact)
        
        if abs(c**3 - c_cubed_needed) < 1e-10:
            if (c > 0 and c < b and c < a and c < d and 
                c != a and c != b and c != d):
                
                if abs(a**3 + b**3 + c**3 - d**3) < 1e-10:
                    quadruplet = (a, b, c, d)
                    quadruplets.append(quadruplet)
                    
                    # ENHANCED: Analyze common factors
                    if include_factors:
                        common_factor = find_gcd_multiple(a, b, c, d)
                        is_primitive = common_factor == 1
                        
                        if is_primitive:
                            primitive_solutions.append(quadruplet)
                            primitive_a, primitive_b, primitive_c, primitive_d = a, b, c, d
                        else:
                            primitive_a, primitive_b, primitive_c, primitive_d, _ = get_primitive_form(a, b, c, d)
                        
                        # Group by primitive form
                        primitive_key = (primitive_a, primitive_b, primitive_c, primitive_d)
                        if primitive_key not in factor_families:
                            factor_families[primitive_key] = []
                        factor_families[primitive_key].append((quadruplet, common_factor))
                    
                    search_details += f"""
✅ **FOUND QUADRUPLET #{len(quadruplets)}: ({a}, {b}, {c}, {d})**
🧮 **Basic verification:**
   • {a}³ + {b}³ + {c}³ = {a**3:,} + {b**3:,} + {c**3:,} = {a**3 + b**3 + c**3:,}
   • {d}³ = {d**3:,} ✓
"""
                    
                    # ENHANCED: Add factor analysis
                    if include_factors:
                        search_details += f"""🔢 **Factor Analysis:**
   • Common factor: {common_factor}
   • Type: {'Primitive' if is_primitive else 'Non-primitive'}
   • Primitive form: ({primitive_a}, {primitive_b}, {primitive_c}, {primitive_d})
"""
                        if not is_primitive:
                            search_details += f"   • Scaling: {common_factor} × ({primitive_a}, {primitive_b}, {primitive_c}, {primitive_d})\n"
    
    # ENHANCED: Generate additional solutions using found primitives
    if include_factors and primitive_solutions:
        search_details += f"\n🚀 **GENERATING FACTOR FAMILIES:**\n"
        generated_count = 0
        
        for primitive in primitive_solutions:
            prim_a, prim_b, prim_c, prim_d = primitive
            search_details += f"\n📊 **From primitive ({prim_a}, {prim_b}, {prim_c}, {prim_d}):**\n"
            
            for factor in range(2, max_factor + 1):
                new_a, new_b, new_c, new_d = factor * prim_a, factor * prim_b, factor * prim_c, factor * prim_d
                
                # Check if this scaled solution fits our original constraint (d = a + n)
                if new_d == new_a + (factor * (prim_d - prim_a)):
                    # Add to results if not already found
                    scaled_solution = (new_a, new_b, new_c, new_d)
                    if scaled_solution not in quadruplets:
                        quadruplets.append(scaled_solution)
                        generated_count += 1
                        
                        search_details += f"   • Factor {factor}: ({new_a}, {new_b}, {new_c}, {new_d})\n"
                        search_details += f"     Verification: {new_a}³ + {new_b}³ + {new_c}³ = {new_d}³ ✓\n"
        
        if generated_count > 0:
            search_details += f"\n🎉 **Generated {generated_count} additional solutions from scaling!**\n"
    
    # ENHANCED: Summary with factor analysis
    if not quadruplets:
        result_text += f"\n❌ **No cube quadruplets found**\n"
    else:
        result_text += search_details
        result_text += f"\n🎉 **ENHANCED SUMMARY:**\n"
        result_text += f"• Total quadruplets found: {len(quadruplets)}\n"
        
        if include_factors:
            result_text += f"• Primitive solutions: {len(primitive_solutions)}\n"
            result_text += f"• Factor families: {len(factor_families)}\n"
            
            if factor_families:
                result_text += f"\n🏠 **SOLUTION FAMILIES:**\n"
                for i, (primitive_key, family_members) in enumerate(factor_families.items(), 1):
                    result_text += f"{i}. Primitive: {primitive_key}\n"
                    for member, factor in family_members:
                        result_text += f"   • Factor {factor}: {member}\n"
    
    return result_text, quadruplets

def find_cube_quadruplets_range_with_factors(a_start, a_end, n_start, n_end, max_iterations_per_combo=5000, 
                                           focus_on_primitives=True, max_factor=3):
    """
    ENHANCED: Range search with primitive-first approach
    """
    try:
        a_start, a_end = int(a_start), int(a_end)
        n_start, n_end = int(n_start), int(n_end)
        max_iterations_per_combo = int(max_iterations_per_combo) if max_iterations_per_combo > 0 else 5000
        max_factor = int(max_factor) if max_factor > 0 else 3
    except (ValueError, TypeError):
        return "Error: Please enter valid integers", []
    
    if a_start <= 0 or a_end <= 0 or n_start <= 0 or n_end <= 0:
        return "Error: All values must be positive integers", []
    
    if a_start > a_end:
        a_start, a_end = a_end, a_start
    if n_start > n_end:
        n_start, n_end = n_end, n_start
    
    result_text = f"""🔍 **ENHANCED RANGE SEARCH WITH FACTOR ANALYSIS:**
📊 **Search Parameters:**
• a range: {a_start} to {a_end}
• n range: {n_start} to {n_end}
• Focus on primitives: {'Yes' if focus_on_primitives else 'No'}
• Max scaling factor: {max_factor}
{'='*80}
"""
    
    all_quadruplets = []
    primitive_solutions = []
    
    # ENHANCED: Two-phase search
    if focus_on_primitives:
        result_text += "\n🎯 **PHASE 1: Finding Primitive Solutions**\n"
        
        # Phase 1: Search for primitive solutions
        for a in range(a_start, a_end + 1):
            for n in range(n_start, n_end + 1):
                search_result, found_quadruplets = find_cube_quadruplets_with_factors(
                    a, n, max_iterations_per_combo, include_factors=True, max_factor=1
                )
                
                for quad in found_quadruplets:
                    if is_primitive_solution(*quad) and quad not in all_quadruplets:
                        all_quadruplets.append(quad)
                        primitive_solutions.append(quad)
                        result_text += f"✅ Primitive: {quad}\n"
        
        result_text += f"\n🏆 **Found {len(primitive_solutions)} primitive solutions**\n"
        
        # Phase 2: Generate scaled families
        if primitive_solutions:
            result_text += f"\n🚀 **PHASE 2: Generating Scaled Families**\n"
            
            for primitive in primitive_solutions:
                prim_a, prim_b, prim_c, prim_d = primitive
                original_n = prim_d - prim_a
                
                result_text += f"\n📊 **Scaling primitive {primitive}:**\n"
                
                for factor in range(2, max_factor + 1):
                    scaled_quad = tuple(factor * x for x in primitive)
                    scaled_a, scaled_b, scaled_c, scaled_d = scaled_quad
                    scaled_n = scaled_d - scaled_a
                    
                    # Check if scaled solution is within our search range
                    if (a_start <= scaled_a <= a_end and 
                        n_start <= scaled_n <= n_end and 
                        scaled_quad not in all_quadruplets):
                        
                        all_quadruplets.append(scaled_quad)
                        result_text += f"   • Factor {factor}: {scaled_quad} (a={scaled_a}, n={scaled_n})\n"
    
    else:
        # Original range search without primitive focus
        result_text += "\n🔍 **STANDARD RANGE SEARCH:**\n"
        for a in range(a_start, a_end + 1):
            for n in range(n_start, n_end + 1):
                search_result, found_quadruplets = find_cube_quadruplets_with_factors(
                    a, n, max_iterations_per_combo, include_factors=True, max_factor=max_factor
                )
                all_quadruplets.extend(found_quadruplets)
    
    # Final summary
    result_text += f"\n{'='*80}\n"
    result_text += f"🎉 **FINAL SUMMARY:**\n"
    result_text += f"• Total quadruplets found: {len(all_quadruplets)}\n"
    result_text += f"• Primitive solutions: {len(primitive_solutions)}\n"
    
    if all_quadruplets:
        result_text += f"\n🏆 **ALL SOLUTIONS FOUND:**\n"
        for i, quad in enumerate(all_quadruplets, 1):
            factor = find_gcd_multiple(*quad)
            is_prim = factor == 1
            result_text += f"{i:2d}. {quad} {'(Primitive)' if is_prim else f'(Factor: {factor})'}\n"
    
    return result_text, all_quadruplets

def create_improved_interface():
    """
    ENHANCED: Interface with common factor analysis
    """
    
    with gr.Blocks(title="KK's Enhanced Cube Quadruplets Finder with Common Factors") as demo:
        
        gr.Markdown("""
        # 🔢 KK's Enhanced Cube Quadruplets Finder with Common Factors 🔢
        ### Find solutions to: **d³ - a³ = b³ + c³** (where d = a + n)
        #### Alternative form: **a³ + b³ + c³ = d³**
        *Constraint: d > a > b > c > 0 (all positive, distinct integers)*
        
        ### 🆕 **New Features:**
        - **Common Factor Analysis**: Identify primitive vs scaled solutions
        - **Solution Families**: Group solutions by their primitive forms
        - **Intelligent Scaling**: Generate additional solutions from primitives
        """)
        
        with gr.Tabs():
            # ENHANCED Tab 1: Range search with factors
            with gr.Tab("🎯 Enhanced Range Search"):
                gr.Markdown("""
                ### 🚀 Smart range search with primitive-first approach
                **Find primitive solutions first, then generate scaled families**
                """)
                
                with gr.Row():
                    with gr.Column():
                        a_start_input = gr.Number(label="'a' start value", value=1, precision=0)
                        a_end_input = gr.Number(label="'a' end value", value=8, precision=0)
                        n_start_input = gr.Number(label="'n' start value", value=1, precision=0)
                        n_end_input = gr.Number(label="'n' end value", value=5, precision=0)
                        max_iter_range = gr.Number(label="Max iterations per combination", value=3000, precision=0)
                        focus_primitives = gr.Checkbox(label="Focus on primitives first", value=True)
                        max_scale_factor = gr.Number(label="Max scaling factor", value=4, precision=0)
                        enhanced_range_search_btn = gr.Button("🎯 Start Enhanced Range Search", variant="primary")
                    
                    with gr.Column():
                        enhanced_range_output = gr.Textbox(label="Enhanced Range Search Results", lines=20, max_lines=25)
                
                # FIXED: Results table and download section
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📊 **Results Table (a, b, c, d in separate columns)**")
                        results_table = gr.Dataframe(
                            headers=["No.", "a", "b", "c", "d", "n", "Factor", "Type", "Primitive Form"],
                            label="Found Quadruplets",
                            wrap=True
                        )
                    
                    with gr.Column():
                        gr.Markdown("### 📥 **Download Results**") 
                        download_btn = gr.Button("📥 Download Excel File", variant="secondary")
                        download_file = gr.File(label="Excel Download", visible=False)
                        download_status = gr.Textbox(label="Download Status", visible=True, interactive=False)
                
                enhanced_quadruplets_state = gr.State([])
                
                def update_results_table(quadruplets):
                    """Update the results table with found quadruplets"""
                    if not quadruplets:
                        return []
                    
                    table_data = []
                    for i, (a, b, c, d) in enumerate(quadruplets, 1):
                        common_factor = find_gcd_multiple(a, b, c, d)
                        is_primitive = common_factor == 1
                        
                        if is_primitive:
                            primitive_form = f"({a}, {b}, {c}, {d})"
                        else:
                            prim_a, prim_b, prim_c, prim_d, _ = get_primitive_form(a, b, c, d)
                            primitive_form = f"({prim_a}, {prim_b}, {prim_c}, {prim_d})"
                        
                        table_data.append([
                            i, a, b, c, d, d-a, common_factor,
                            'Primitive' if is_primitive else 'Scaled',
                            primitive_form
                        ])
                    
                    return table_data
                
                def download_excel_file(quadruplets):
                    """Generate Excel file for download"""
                    if not quadruplets:
                        return None, "❌ No data to download"
                    
                    try:
                        excel_data = export_to_excel(quadruplets)
                        if excel_data:
                            # Save to temporary file
                            import tempfile
                            import os
                            
                            # Create temporary file
                            temp_fd, temp_path = tempfile.mkstemp(suffix='.xlsx', prefix='cube_quadruplets_')
                            
                            # Write data to temporary file
                            with os.fdopen(temp_fd, 'wb') as tmp_file:
                                tmp_file.write(excel_data)
                            
                            return temp_path, f"✅ Excel file ready! Found {len(quadruplets)} solutions"
                        else:
                            return None, "❌ Failed to generate Excel file"
                    except Exception as e:
                        return None, f"❌ Error: {str(e)}"
                
                enhanced_range_search_btn.click(
                    find_cube_quadruplets_range_with_factors,
                    inputs=[a_start_input, a_end_input, n_start_input, n_end_input, 
                           max_iter_range, focus_primitives, max_scale_factor],
                    outputs=[enhanced_range_output, enhanced_quadruplets_state]
                ).then(
                    update_results_table,
                    inputs=[enhanced_quadruplets_state],
                    outputs=[results_table]
                )
                
                download_btn.click(
                    download_excel_file,
                    inputs=[enhanced_quadruplets_state],
                    outputs=[download_file, download_status]
                )
            
            # ENHANCED Tab 2: Single search with factors
            with gr.Tab("🚀 Enhanced Single Search"):
                gr.Markdown("""
                ### 🎯 Single search with common factor analysis
                **Find solutions and analyze their primitive forms**
                """)
                
                with gr.Row():
                    with gr.Column():
                        a_input = gr.Number(label="Value of 'a' (positive integer)", value=6, precision=0)
                        n_input = gr.Number(label="Value of 'n' (positive integer)", value=3, precision=0)
                        max_iter = gr.Number(label="Max iterations", value=20000, precision=0)
                        include_factors = gr.Checkbox(label="Include factor analysis", value=True)
                        max_factor = gr.Number(label="Max factor for scaling", value=5, precision=0)
                        enhanced_search_btn = gr.Button("🚀 Start Enhanced Search", variant="primary")
                    
                    with gr.Column():
                        enhanced_search_output = gr.Textbox(label="Enhanced Search Results", lines=25, max_lines=30)
                
                enhanced_single_quadruplets_state = gr.State([])
                
                enhanced_search_btn.click(
                    find_cube_quadruplets_with_factors,
                    inputs=[a_input, n_input, max_iter, include_factors, max_factor],
                    outputs=[enhanced_search_output, enhanced_single_quadruplets_state]
                )
            
            # Additional Tab: Known Solutions Test
            with gr.Tab("🧪 Known Solutions Test"):
                gr.Markdown("""
                ### 🧪 Test with known solutions
                **Verify the algorithm works with known cube quadruplets**
                """)
                
                with gr.Row():
                    with gr.Column():
                        test_btn = gr.Button("🧪 Test Known Solutions", variant="primary")
                    
                    with gr.Column():
                        test_output = gr.Textbox(label="Test Results", lines=15)
                
                def test_known_solutions():
                    """Test with some known solutions"""
                    known_tests = [
                        (6, 3),  # Should find (6, 8, 10, 9)
                        (15, 18), # Should find larger solutions
                        (3, 3),   # Test smaller values
                    ]
                    
                    test_results = "🧪 **TESTING KNOWN SOLUTIONS:**\n" + "="*50 + "\n"
                    
                    for i, (a, n) in enumerate(known_tests, 1):
                        test_results += f"\n🔍 **Test {i}: a={a}, n={n}**\n"
                        result, quadruplets = find_cube_quadruplets_with_factors(a, n, 15000, True, 3)
                        
                        if quadruplets:
                            test_results += f"✅ Found {len(quadruplets)} solutions:\n"
                            for quad in quadruplets:
                                factor = find_gcd_multiple(*quad)
                                is_prim = factor == 1
                                test_results += f"   • {quad} {'(Primitive)' if is_prim else f'(Factor: {factor})'}\n"
                        else:
                            test_results += "❌ No solutions found\n"
                        
                        test_results += "-" * 40 + "\n"
                    
                    return test_results
                
                test_btn.click(
                    test_known_solutions,
                    outputs=[test_output]
                )
    
    return demo

if __name__ == "__main__":
    try:
        print("🚀 Creating enhanced Gradio interface with common factors...")
        demo = create_improved_interface()
        print("🎉 Launching enhanced cube quadruplets finder...")
        demo.launch(share=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please ensure Gradio is installed: pip install gradio")
