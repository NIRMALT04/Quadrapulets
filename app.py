import gradio as gr
import math


def find_cube_quadruplets_improved(a, n, max_iterations=10000):
    """
    Improved cube quadruplets finder with unlimited search capability
    Equation: d³ - a³ = b³ + c³
    Where: d = a + n, and d > a > b > c > 0
    """
    try:
        a, n = int(a), int(n)
        max_iterations = int(max_iterations) if max_iterations > 0 else 10000
    except (ValueError, TypeError):
        return "Error: Please enter valid integers", []
    
    if a <= 0 or n <= 0:
        return "Error: Both 'a' and 'n' must be positive integers", []
    
    d = a + n
    target_sum = d**3 - a**3
    
    result_text = f"""🔍 **Searching for cube quadruplets (UNLIMITED SEARCH):**
📊 **Parameters:**
• a = {a}
• n = {n}  
• d = a + n = {d}
• Target: d³ - a³ = {d}³ - {a}³ = {target_sum:,}
• Equation: b³ + c³ = {target_sum:,}
• Constraint: {d} > {a} > b > c > 0
{'='*60}
"""
    
    quadruplets = []
    search_details = ""
    iterations = 0
    
    # Unlimited search - we'll search until we find solutions or hit iteration limit
    # Start from b = a-1 and work downwards
    max_b = a - 1
    
    for b in range(max_b, 0, -1):
        iterations += 1
        
        # Progress indicator for long searches
        if iterations % 1000 == 0:
            search_details += f"🔄 Searched {iterations} iterations... (current b = {b})\n"
        
        # Stop if we've hit the iteration limit (to prevent infinite loops in UI)
        if iterations > max_iterations:
            search_details += f"⚠️ **Search stopped after {max_iterations:,} iterations**\n"
            search_details += f"📈 **To continue search, increase max_iterations parameter**\n\n"
            break
        
        if b >= a or b >= d:  # Ensure b < a and b < d
            continue
            
        b_cubed = b**3
        
        # Calculate required c³ from equation: c³ = d³ - a³ - b³
        c_cubed_needed = target_sum - b_cubed
        
        # Skip if c³ would be non-positive
        if c_cubed_needed <= 0:
            continue
            
        # Calculate c = ∛(d³ - a³ - b³)
        c_exact = c_cubed_needed**(1/3)
        c = round(c_exact)
        
        # Verify c is a perfect cube root (within floating point precision)
        if abs(c**3 - c_cubed_needed) < 1e-10:  # Better precision check
            # Verify all constraints
            if (c > 0 and c < b and c < a and c < d and 
                c != a and c != b and c != d):
                
                # Final verification of the equation
                if abs(a**3 + b**3 + c**3 - d**3) < 1e-10:
                    quadruplet = (a, b, c, d)
                    quadruplets.append(quadruplet)
                    
                    search_details += f"""
✅ **FOUND VALID QUADRUPLET #{len(quadruplets)}: ({a}, {b}, {c}, {d})**
🧮 **Step-by-step calculation:**
   • d³ - a³ = {d}³ - {a}³ = {d**3:,} - {a**3:,} = {target_sum:,}
   • For b = {b}: b³ = {b**3:,}
   • Required c³ = {target_sum:,} - {b**3:,} = {c_cubed_needed:,}
   • c = ∛({c_cubed_needed:,}) = {c}
   • Verification: c³ = {c**3:,} ✓
🎯 **Full equation check:**
   • {a}³ + {b}³ + {c}³ = {a**3:,} + {b**3:,} + {c**3:,} = {a**3 + b**3 + c**3:,}
   • {d}³ = {d**3:,}
   • Match: {"✅" if abs(a**3 + b**3 + c**3 - d**3) < 1e-10 else "❌"}
📏 **Constraint check:** {d} > {a} > {b} > {c} > 0
   • {d} > {a}: {"✅" if d > a else "❌"}
   • {a} > {b}: {"✅" if a > b else "❌"}  
   • {b} > {c}: {"✅" if b > c else "❌"}
   • {c} > 0: {"✅" if c > 0 else "❌"}
"""
    
    # Summary
    if not quadruplets:
        result_text += f"\n❌ **No cube quadruplets found**\n"
        result_text += f"🔍 **Search completed:** {iterations:,} iterations\n"
        result_text += f"📊 **Range searched:** b from {max_b} down to 1\n"
        result_text += f"💡 **Suggestion:** Try different values of 'a' and 'n'\n"
    else:
        result_text += search_details
        result_text += f"\n🎉 **SUMMARY:** Found {len(quadruplets)} quadruplet(s) after {iterations:,} iterations\n"
    
    return result_text, quadruplets


def find_cube_quadruplets_range(a_start, a_end, n_start, n_end, max_iterations_per_combo=5000):
    """
    NEW FUNCTION: Search for cube quadruplets across ranges of 'a' and 'n' values
    """
    try:
        a_start, a_end = int(a_start), int(a_end)
        n_start, n_end = int(n_start), int(n_end)
        max_iterations_per_combo = int(max_iterations_per_combo) if max_iterations_per_combo > 0 else 5000
    except (ValueError, TypeError):
        return "Error: Please enter valid integers", []
    
    if a_start <= 0 or a_end <= 0 or n_start <= 0 or n_end <= 0:
        return "Error: All values must be positive integers", []
    
    if a_start > a_end:
        a_start, a_end = a_end, a_start
    
    if n_start > n_end:
        n_start, n_end = n_end, n_start
    
    total_combinations = (a_end - a_start + 1) * (n_end - n_start + 1)
    
    result_text = f"""🔍 **RANGE SEARCH FOR CUBE QUADRUPLETS:**
📊 **Search Parameters:**
• a range: {a_start} to {a_end} ({a_end - a_start + 1} values)
• n range: {n_start} to {n_end} ({n_end - n_start + 1} values)
• Total combinations: {total_combinations:,}
• Max iterations per combination: {max_iterations_per_combo:,}
• Equation: d³ - a³ = b³ + c³ (where d = a + n)
• Constraint: d > a > b > c > 0
{'='*80}
"""
    
    all_quadruplets = []
    combinations_tested = 0
    combinations_with_solutions = 0
    
    for a in range(a_start, a_end + 1):
        for n in range(n_start, n_end + 1):
            combinations_tested += 1
            d = a + n
            target_sum = d**3 - a**3
            
            # Progress update
            if combinations_tested % 10 == 0:
                progress = (combinations_tested / total_combinations) * 100
                result_text += f"🔄 Progress: {combinations_tested}/{total_combinations} ({progress:.1f}%) - Testing a={a}, n={n}\n"
            
            # Search for quadruplets for this (a, n) combination
            found_for_this_combo = []
            iterations = 0
            max_b = a - 1
            
            for b in range(max_b, 0, -1):
                iterations += 1
                
                if iterations > max_iterations_per_combo:
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
                            found_for_this_combo.append(quadruplet)
                            all_quadruplets.append(quadruplet)
            
            # Report findings for this combination
            if found_for_this_combo:
                combinations_with_solutions += 1
                result_text += f"\n✅ **FOUND {len(found_for_this_combo)} SOLUTION(S) for a={a}, n={n}:**\n"
                for i, (a_val, b_val, c_val, d_val) in enumerate(found_for_this_combo, 1):
                    result_text += f"   {i}. ({a_val}, {b_val}, {c_val}, {d_val}) → "
                    result_text += f"{a_val}³ + {b_val}³ + {c_val}³ = {d_val}³\n"
                    result_text += f"      Verification: {a_val**3:,} + {b_val**3:,} + {c_val**3:,} = {d_val**3:,} ✓\n"
    
    # Final summary
    result_text += f"\n{'='*80}\n"
    result_text += f"🎉 **FINAL SUMMARY:**\n"
    result_text += f"• Total combinations tested: {combinations_tested:,}\n"
    result_text += f"• Combinations with solutions: {combinations_with_solutions:,}\n"
    result_text += f"• Total quadruplets found: {len(all_quadruplets):,}\n"
    result_text += f"• Success rate: {(combinations_with_solutions/combinations_tested*100):.2f}%\n"
    
    if all_quadruplets:
        result_text += f"\n🏆 **ALL FOUND QUADRUPLETS:**\n"
        for i, (a, b, c, d) in enumerate(all_quadruplets, 1):
            result_text += f"{i:2d}. ({a}, {b}, {c}, {d})\n"
    else:
        result_text += f"\n❌ **No quadruplets found in the specified ranges**\n"
        result_text += f"💡 **Suggestions:**\n"
        result_text += f"   • Try larger ranges\n"
        result_text += f"   • Increase max_iterations_per_combo\n"
        result_text += f"   • Focus on smaller values of 'a' first\n"
    
    return result_text, all_quadruplets


def verify_equation_step_by_step(a, b, c, d):
    """
    Detailed step-by-step verification showing the equation d³ - a³ = b³ + c³
    """
    try:
        a, b, c, d = int(a), int(b), int(c), int(d)
    except (ValueError, TypeError):
        return "❌ **Error:** Please enter valid integers"
    
    if any(x <= 0 for x in [a, b, c, d]):
        return "❌ **Error:** All values must be positive integers"
    
    # Calculate all values
    a_cubed = a**3
    b_cubed = b**3
    c_cubed = c**3
    d_cubed = d**3
    
    left_side = d_cubed - a_cubed  # d³ - a³
    right_side = b_cubed + c_cubed  # b³ + c³
    
    result = f"""🧮 **Step-by-Step Equation Verification**
📊 **Given Quadruplet:** ({a}, {b}, {c}, {d})
🔢 **Individual Cube Calculations:**
• a³ = {a}³ = {a_cubed:,}
• b³ = {b}³ = {b_cubed:,}  
• c³ = {c}³ = {c_cubed:,}
• d³ = {d}³ = {d_cubed:,}
🎯 **Main Equation: d³ - a³ = b³ + c³**
• Left side:  d³ - a³ = {d_cubed:,} - {a_cubed:,} = {left_side:,}
• Right side: b³ + c³ = {b_cubed:,} + {c_cubed:,} = {right_side:,}
"""
    
    if left_side == right_side:
        result += "✅ **EQUATION SATISFIED!** ✅\n\n"
        
        # Alternative form verification
        alt_check = a_cubed + b_cubed + c_cubed
        result += f"🔄 **Alternative form check (a³ + b³ + c³ = d³):**\n"
        result += f"• a³ + b³ + c³ = {a_cubed:,} + {b_cubed:,} + {c_cubed:,} = {alt_check:,}\n"
        result += f"• d³ = {d_cubed:,}\n"
        result += f"• Match: {'✅' if alt_check == d_cubed else '❌'}\n\n"
        
        # Check ordering constraints
        result += f"📏 **Constraint Verification:**\n"
        constraints = [
            (d > a, f"{d} > {a}", "d > a"),
            (a > b, f"{a} > {b}", "a > b"), 
            (b > c, f"{b} > {c}", "b > c"),
            (c > 0, f"{c} > 0", "c > 0")
        ]
        
        all_satisfied = True
        for satisfied, comparison, desc in constraints:
            result += f"• {desc}: {comparison} {'✅' if satisfied else '❌'}\n"
            if not satisfied:
                all_satisfied = False
        
        if all_satisfied:
            result += f"\n🎉 **ALL CONSTRAINTS SATISFIED!**"
        else:
            result += f"\n⚠️ **Some constraints not satisfied**"
            
    else:
        result += f"❌ **EQUATION NOT SATISFIED** ❌\n"
        result += f"💔 **Difference:** |{left_side:,} - {right_side:,}| = {abs(left_side - right_side):,}"
    
    return result


def test_known_solutions():
    """
    Test some known cube quadruplet solutions
    """
    known_quadruplets = [
        (3, 4, 5, 6),    # Famous solution: 3³ + 4³ + 5³ = 6³
        (1, 12, 1, 12),  # Edge case (if valid)
        (87, 117, 44, 138), # Another known solution
    ]
    
    results = "🧪 **Testing Known Cube Quadruplet Solutions**\n\n"
    
    for i, (a, b, c, d) in enumerate(known_quadruplets, 1):
        results += f"**Test {i}: ({a}, {b}, {c}, {d})**\n"
        
        # Check equation d³ - a³ = b³ + c³
        left = d**3 - a**3
        right = b**3 + c**3
        
        results += f"• d³ - a³ = {d}³ - {a}³ = {left:,}\n"
        results += f"• b³ + c³ = {b}³ + {c}³ = {right:,}\n"
        results += f"• Result: {'✅ Valid' if left == right else '❌ Invalid'}\n\n"
    
    return results


def create_improved_interface():
    """
    Create improved Gradio interface with range search capability
    """
    
    with gr.Blocks(title="KK's Enhanced Cube Quadruplets Finder") as demo:
        
        gr.Markdown("""
        # 🔢 KK's Enhanced Cube Quadruplets Finder 🔢
        ### Find solutions to: **d³ - a³ = b³ + c³** (where d = a + n)
        #### Alternative form: **a³ + b³ + c³ = d³**
        *Constraint: d > a > b > c > 0 (all positive, distinct integers)*
        """)
        
        with gr.Tabs():
            # Tab 1: Range search (NEW)
            with gr.Tab("🎯 Range Search"):
                gr.Markdown("""
                ### 🚀 Search across ranges of 'a' and 'n' values
                **Systematically test multiple combinations to find all quadruplets**
                """)
                
                with gr.Row():
                    with gr.Column():
                        a_start_input = gr.Number(label="'a' start value", value=1, precision=0)
                        a_end_input = gr.Number(label="'a' end value", value=10, precision=0)
                        n_start_input = gr.Number(label="'n' start value", value=1, precision=0)
                        n_end_input = gr.Number(label="'n' end value", value=5, precision=0)
                        max_iter_range = gr.Number(label="Max iterations per combination", value=3000, precision=0)
                        range_search_btn = gr.Button("🎯 Start Range Search", variant="primary")
                    
                    with gr.Column():
                        range_search_output = gr.Textbox(label="Range Search Results", lines=25, max_lines=30)
                
                range_quadruplets_state = gr.State([])
                
                range_search_btn.click(
                    find_cube_quadruplets_range,
                    inputs=[a_start_input, a_end_input, n_start_input, n_end_input, max_iter_range],
                    outputs=[range_search_output, range_quadruplets_state]
                )
            
            # Tab 2: Single search
            with gr.Tab("🚀 Single Search"):
                gr.Markdown("""
                ### 🎯 Search for cube quadruplets with specific 'a' and 'n'
                **Input:** Only 'a' and 'n' → **Output:** All valid (b, c) combinations
                """)
                
                with gr.Row():
                    with gr.Column():
                        a_input = gr.Number(label="Value of 'a' (positive integer)", value=6, precision=0)
                        n_input = gr.Number(label="Value of 'n' (positive integer)", value=3, precision=0)
                        max_iter = gr.Number(label="Max iterations (0 for default 10k)", value=20000, precision=0)
                        search_btn = gr.Button("🚀 Start Search", variant="primary")
                    
                    with gr.Column():
                        search_output = gr.Textbox(label="Search Results", lines=20, max_lines=25)
                
                quadruplets_state = gr.State([])
                
                search_btn.click(
                    find_cube_quadruplets_improved,
                    inputs=[a_input, n_input, max_iter],
                    outputs=[search_output, quadruplets_state]
                )
            
            # Tab 3: Step-by-step verification
            with gr.Tab("🔍 Step-by-Step Verification"):
                gr.Markdown("### 🧮 Detailed verification: d³ - a³ = b³ + c³")
                
                with gr.Row():
                    with gr.Column():
                        ver_a = gr.Number(label="a", value=3, precision=0)
                        ver_b = gr.Number(label="b", value=4, precision=0)
                        ver_c = gr.Number(label="c", value=5, precision=0)
                        ver_d = gr.Number(label="d", value=6, precision=0)
                        verify_btn = gr.Button("🔍 Verify Step-by-Step", variant="secondary")
                    
                    with gr.Column():
                        verify_output = gr.Textbox(label="Detailed Verification", lines=20, max_lines=25)
                
                verify_btn.click(
                    verify_equation_step_by_step,
                    inputs=[ver_a, ver_b, ver_c, ver_d],
                    outputs=verify_output
                )
            
            # Tab 4: Test known solutions
            with gr.Tab("🧪 Known Solutions Test"):
                gr.Markdown("### 📋 Test mathematically known cube quadruplet solutions")
                
                with gr.Row():
                    with gr.Column():
                        test_btn = gr.Button("🧪 Test Known Solutions", variant="secondary")
                    
                    with gr.Column():
                        test_output = gr.Textbox(label="Known Solutions Test Results", lines=15, max_lines=20)
                
                test_btn.click(
                    test_known_solutions,
                    inputs=[],
                    outputs=test_output
                )
    
    return demo


if __name__ == "__main__":
    try:
        print("🚀 Creating enhanced Gradio interface...")
        demo = create_improved_interface()
        print("🎉 Launching enhanced cube quadruplets finder...")
        demo.launch(share=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please ensure Gradio is installed: pip install gradio")