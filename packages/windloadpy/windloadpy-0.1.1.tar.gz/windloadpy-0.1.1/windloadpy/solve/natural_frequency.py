import math

def natural_frequency(material_type, mean_height):
    report = ""

    if material_type == "concrete":
        report += "<h4>For Concrete buildings</h4>"
        na = 14.93 / math.pow(mean_height,0.9)
        report += f"<center> \\( n_{{ a }} = \\frac {{ 14.93 }}{{ \\text{{h}}^{{0.9}} }} \\) </center>"
        report += f"<center> \\( n_{{a }} =  \\frac {{ 14.93 }}{{ \\left( {mean_height:.2f} \\right)^{{0.9}} }} \\) </center>"
    elif material_type == "steel":
        report += "<h4>For structural steel moment-resisting-frame buildings</h4>"
        na = 8.58 / math.pow(mean_height,0.8)
        report += f"<center> \\( n_{{ a }} = \\frac {{ 8.58 }}{{ \\text{{h}}^{{0.8}} }} \\) </center>"
        report += f"<center> \\( n_{{ a }} = \\frac {{ 8.58 }}{{ \\left( {mean_height:.2f} \\right)^{{0.8}} }} \\) </center>"
    elif material_type == "others":
        na = 22.86 / mean_height
        report += f"<center> \\( n_{{ a }} = \\frac {{ 22.86 }}{{ \\text{{h}} }} \\) </center>"
        report += f"<center> \\( n_{{ a }} = \\frac {{ 22.86 }}{{ {mean_height:.2f} }} \\) </center>"

    behavior = "rigid" if na >= 1.0 else "flexible"
    # report += f"<center>\\( n_{{a}}  = {na:.3f} \\therefore \\text{{Structure is  {remarks}}} \\)</center>"
 
    return {
        "report": report,
        "value": na,
        "unit" : "hz",
        "behavior": behavior
    }


