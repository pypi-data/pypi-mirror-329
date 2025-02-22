import math

def radtodegree():
    results = 180 / math.pi
    return results

def header():
    results = """
        <h1><center><strong>WIND CALCULATION REPORT</strong></center></h1>
        <h2>Reference</h2>
        <ul>
            <li>Association of Structural Engineers of the Philippines 2015 Edition, National Structural Code of the Philippines Volume 1, Quezon City, Philippines.</li>
            <li>American Society of Civil Engineering, ASCE 7-10, USA</li>
            </ul>
        """
    return results
