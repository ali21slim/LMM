import json

# Load the list from the JSON file
with open("midi_values_sample1.json", "r") as f:
    onsetFrequenciesInMidiValues = json.load(f)

# print(onsetFrequenciesInMidiValues)





# COMPLEXITY IS O(n) 
# Z[i] is the longest prefix match strating from position i
def Z_Algorithm(s):
    n=len(s)
    Z = [0]*n
    # left points to the first index of the Z-Box
    # right points to the last index of the Z-Box
    left = 0
    right = 0
    K = 0
    # for example []
    for i in range(1,n):

        if i>right: # we are moving outside the window
            left,right = i , i

            while right<n and s[right]==s[right-left]:
                right+=1
            Z[i] = right-left # Size of the Z-Box which is repeated
            right-=1 # we decremenet right by 1 because it was pointing to an unmatching element

        else: # we are moving inside the window
            K = i-left
            # we use the values already computed before to avoid repeating the same operations
            if Z[K] < right - i + 1: # we are checking if the match lenght Z[K] is smaller than the remaining part of the current window
                Z[i]=Z[K] # we can use the previously computed match
            
            else: # Full Match so we need to expand the Z-Box
                left=i

                while right<n and s[right]==s[right-left]:
                    right+=1
                Z[i] = right-left # The new Size of the Z-Box which is repeated
                right-=1 # we decremenet right by 1 because it was pointing to an unmatching element
    return Z

def midi_to_note(midi_value):
    if 40 <= midi_value <= 50:
        return "Doum"
    elif 65 <= midi_value <= 75:
        return "Tak"
    elif 55 <= midi_value <= 65:
        return "Ka"
    else:
        return "Unknown"


def detect_cycles(freq_list, period_threshold=2):
    Z = Z_Algorithm(freq_list)
    n = len(freq_list)
    cycles = []

    for i in range(1, n):
        if Z[i] >= period_threshold:
            period = i
            cycles.append((period, freq_list[:period]))
            # print(f"Detected Cycle: Period {period}, {freq_list[:period]}")  # Debugging

    return cycles


# Map frequencies to darbuka notes
def map_to_notes(frequencies):
    return [midi_to_note(freq) for freq in frequencies]


# Run detection and output results
detected_cycles = detect_cycles(onsetFrequenciesInMidiValues)
output_file = "Cycles_Sample1.txt"
with open(output_file, "w") as f:
    if not detected_cycles:
        f.write("No cycles detected.\n")
    else:
        for period, cycle in detected_cycles:
            notes = map_to_notes(cycle)
            f.write(f"Cycle Length: {period}\n")
            f.write(f"Cycle Frequencies: {cycle}\n")
            f.write(f"Notes: {notes}\n\n")

print(f"Cycles saved to {output_file}")
