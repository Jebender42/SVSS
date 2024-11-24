# SVSS - Standardized Visual Sound Spectrum

# IMPORT CODE
import cv2
import numpy as np
import math


# DEFINITIONS

# Function for setting numeric boundaries
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

# 1530 is a value created from moving through the RGB Values starting with R:255 G:0 B:0 
# then moving through all the values to R:255 G:255 B:0
# then R:0 G:255 B:0
# R:0 G:255 B:255
# R:0 G:0 B:255
# R:255 G:0 B:255
# and finally back to R:255 G:0 B:0
# C = Color Value between 0 and 1530 although 1530 and 0 are interpreted as having the same quality of Color. This is the initial Light Spectrum Starting on Red going through ROYGBIV and Circling back around to Red. This represents a Single Octave, or rather Diapason
# K = Dark To Light Fade Value. It is clamped between lowest Note(Sol0) to the Mean Frequency
# F = Light to Dark Fade Value. It is clamped between the Mean Frequency and the Highest Note(Re7)

# RGB Values = interplay of the C, K, and F values in order to define a color along the S axis or Full Spectrum value which goes through several octaves of ROYBIV starting with a totally black note to a totally white note and various shades of ROYBIV that get lighter as notes from higher octaves are used, and darker as notes from lower octaves are used. So essentially the note Do0 is a very dark - almost a totally blacked out Red, and the note Do7 is a very bright note - almost a totally whited out Red. While the Note

# Red Values
def Red(C,K,F):
    if(0 <= C and C < 255):  # If C is between 0 and 255
        return (0 + C)*K + (255 - C)*F  
    elif(255 <= C and C < 765):  # If C is between 255 and 765
        return 255*K 
    elif(765 <= C and C < 1020):   # If C is between 765 and 1020
        return (1020 - C)*K + (C - 765)*F  
    elif(1020 <= C and C < 1530):   # If C is between 1020 and 1530
        return 255*F  
    else:
        return 255

# Green Values
def Green(C,K,F):
    if(0 <= C and C < 510):   # If C is between 0 and 510
        return 255*F   
    elif(510 <= C and C < 765):   # If C is between 510 and 765
        return (C - 510)*K + (765 - C)*F  
    elif(765 <= C and C < 1275):   # If C is between 765 and 1275
        return 255*K  
    elif(1275 <= C and C < 1530):   # If C is between 1275 and 1530
        return (1530 - C)*K + (C - 1275)*F   
    else:
        return 255

# Blue Values
def Blue(C,K,F):
    if(0 <= C and C < 255):   # If C is between 0 and 255
        return 255*K   
    elif(255 <= C and C < 510):   # If C is between 255 and 510
        return (510 - C)*K + (C - 255)*F  
    elif(510 <= C and C < 1020):   # If C is between 510 and 1020
        return 255*F   
    elif(1020 <= C and C < 1275):   # If C is between 1020 and 1275
        return (C - 1020)*K + (1275 - C)*F   
    elif(1275 <= C and C < 1530):   # If C is between 1275 and 1530
        return 255*K   
    else:
        return 255


# The color() funtion utilizes the prior functions to input Length Ratio Value and output RGB Values. The inverse of the Length Value is the Pitch Ratio
def Color_Pitch_Ratio(Pitch_Ratio):
    def linear_interpolation_reverse(P, S_points, P_points):
        for i in range(len(P_points) - 1):
            if P_points[i] <= P <= P_points[i + 1]:
                P1, P2 = P_points[i], P_points[i + 1]
                S1, S2 = S_points[i], S_points[i + 1]
                S = S1 + ((P - P1) * (S2 - S1)) / (P2 - P1)
                return S
        return None  # if P is outside the range of P_points
    
    # Example usage with updated sequences:
    S_points = [0,   147, 179, 510, 637.5, 765, 1020, 1530, 1677, 1709, 2040, 2167.5, 2295, 2550, 3060, 3207, 3239, 3570, 3697.5, 3825, 4080, 4590, 4737, 4769, 5100, 5227.5, 5355, 5610, 6120, 6267, 6299, 6630, 6757.5, 6885, 7140, 7650, 7797, 7829, 8160, 8287.5, 8415,  8670, 9180,  9327, 9359, 9690, 9817.5, 9945, 10200, 10710, 10857, 10889, 11220, 11347.5]
    P_points = [3/4, 5/6, 7/8,   1,   9/8, 5/4,  4/3,  3/2,  5/3,  7/4,     2,   9/4,  5/2,  8/3,    3, 10/3,  7/2,    4,    9/2,    5, 16/3,    6, 20/3,    7,    8,      9,   10, 32/3,   12, 40/3,   14,   16,     18,   20, 64/3,   24, 80/3,   28,   32,     36,   40, 128/3,   48, 160/3,   56,   64,     72,   80, 256/3,    96, 320/3,   112,   128,     144]
    #           Sol0  La0  Te0  Do1    Re1  Mi1   Fa1  Sol1   La1   Te1    Do2    Re2   Mi2   Fa2  Sol2   La2   Te2   Do3     Re3   Mi3   Fa3  Sol3   La3   Te3   Do4     Re4   Mi4   Fa4  Sol4   La4   Te4   Do5     Re5   Mi5   Fa5  Sol5   La5   Te5   Do5     Re5   Mi5    Fa5  Sol5    La5   Te5   Do6     Re6   Mi6    Fa6   Sol6    La6    Te6    Do7      Re7
    
    # To find S for a P value in between the given points
    P = Pitch_Ratio
    S = linear_interpolation_reverse(P, S_points, P_points)
    
    
    C = S % 1530
     # ade.black(K) = Spectrum(S) / (Median S Value) Range(0, 1)
    K = clamp((S / 5673.75), 0, 1)
    # Fde.white(F) = (Spectrum(S) - (Median S Value) / (Median S Value) Range(0, 1)
    F = clamp((S - 5673.75) / (5673.75), 0, 1)

    B = Blue(C,K,F)
    G = Green(C,K,F)
    R = Red(C,K,F)
    color = [B,G,R]
    return color


def Color_Length_Ratio(Length_Ratio):
    def linear_interpolation_reverse(P, S_points, P_points):
        for i in range(len(P_points) - 1):
            if P_points[i] <= P <= P_points[i + 1]:
                P1, P2 = P_points[i], P_points[i + 1]
                S1, S2 = S_points[i], S_points[i + 1]
                S = S1 + ((P - P1) * (S2 - S1)) / (P2 - P1)
                return S
        return None  # if P is outside the range of P_points
    
    # Example usage with updated sequences:
    S_points = [0,   147, 179, 510, 637.5, 765, 1020, 1530, 1677, 1709, 2040, 2167.5, 2295, 2550, 3060, 3207, 3239, 3570, 3697.5, 3825, 4080, 4590, 4737, 4769, 5100, 5227.5, 5355, 5610, 6120, 6267, 6299, 6630, 6757.5, 6885, 7140, 7650, 7797, 7829, 8160, 8287.5, 8415,  8670, 9180,  9327, 9359, 9690, 9817.5, 9945, 10200, 10710, 10857, 10889, 11220, 11347.5]
    P_points = [3/4, 5/6, 7/8,   1,   9/8, 5/4,  4/3,  3/2,  5/3,  7/4,     2,   9/4,  5/2,  8/3,    3, 10/3,  7/2,    4,    9/2,    5, 16/3,    6, 20/3,    7,    8,      9,   10, 32/3,   12, 40/3,   14,   16,     18,   20, 64/3,   24, 80/3,   28,   32,     36,   40, 128/3,   48, 160/3,   56,   64,     72,   80, 256/3,    96, 320/3,   112,   128,     144]
    #           Sol0  La0  Te0  Do1    Re1  Mi1   Fa1  Sol1   La1   Te1    Do2    Re2   Mi2   Fa2  Sol2   La2   Te2   Do3     Re3   Mi3   Fa3  Sol3   La3   Te3   Do4     Re4   Mi4   Fa4  Sol4   La4   Te4   Do5     Re5   Mi5   Fa5  Sol5   La5   Te5   Do5     Re5   Mi5    Fa5  Sol5    La5   Te5   Do6     Re6   Mi6    Fa6   Sol6    La6    Te6    Do7      Re7
    
    # To find S for a P value in between the given points, say P = 5
    P = 1/Length_Ratio
    S = linear_interpolation_reverse(P, S_points, P_points)
    
    C = S % 1530
     # ade.black(K) = Spectrum(S) / (Median S Value) Range(0, 1)
    K = clamp((S / 5673.75), 0, 1)
    # Fde.white(F) = (Spectrum(S) - (Median S Value) / (Median S Value) Range(0, 1)
    F = clamp((S - 5673.75) / (5673.75), 0, 1)

    B = Blue(C,K,F)
    G = Green(C,K,F)
    R = Red(C,K,F)
    color = [B,G,R]
    return color


def Color_Hertz(Hertz_Value):
    def linear_interpolation(P, S_points, P_points):
        for i in range(len(P_points) - 1):
            if P_points[i] <= P <= P_points[i + 1]:
                P1, P2 = P_points[i], P_points[i + 1]
                S1, S2 = S_points[i], S_points[i + 1]
                S = S1 + ((P - P1) * (S2 - S1)) / (P2 - P1)
                return S
        return None  # if P is outside the range of P_points
    
    # Example usage with updated sequences:
    S_points = [0,   147, 179, 510, 637.5, 765, 1020, 1530, 1677, 1709, 2040, 2167.5, 2295, 2550, 3060, 3207, 3239, 3570, 3697.5, 3825, 4080, 4590, 4737, 4769, 5100, 5227.5, 5355, 5610, 6120, 6267, 6299, 6630, 6757.5, 6885, 7140, 7650, 7797, 7829, 8160, 8287.5, 8415,  8670, 9180,  9327, 9359, 9690, 9817.5, 9945, 10200, 10710, 10857, 10889, 11220, 11347.5]
    P_points = [3/4, 5/6, 7/8,   1,   9/8, 5/4,  4/3,  3/2,  5/3,  7/4,     2,   9/4,  5/2,  8/3,    3, 10/3,  7/2,    4,    9/2,    5, 16/3,    6, 20/3,    7,    8,      9,   10, 32/3,   12, 40/3,   14,   16,     18,   20, 64/3,   24, 80/3,   28,   32,     36,   40, 128/3,   48, 160/3,   56,   64,     72,   80, 256/3,    96, 320/3,   112,   128,     144]
    #           Sol0  La0  Te0  Do1    Re1  Mi1   Fa1  Sol1   La1   Te1    Do2    Re2   Mi2   Fa2  Sol2   La2   Te2   Do3     Re3   Mi3   Fa3  Sol3   La3   Te3   Do4     Re4   Mi4   Fa4  Sol4   La4   Te4   Do5     Re5   Mi5   Fa5  Sol5   La5   Te5   Do5     Re5   Mi5    Fa5  Sol5    La5   Te5   Do6     Re6   Mi6    Fa6   Sol6    La6    Te6    Do7      Re7
    
    # To find S for a P value in between the given points, say P = 5
    Half_Step_12_Tet = 2**(1/12)
    La0 = 27.5 #Hertz
    Do1 = La0*(Half_Step_12_Tet**3) #Hertz
    P = Hertz_Value/Do1
    S = linear_interpolation(P, S_points, P_points)
    
    C = S % 1530
     # ade.black(K) = Spectrum(S) / (Median S Value) Range(0, 1)
    K = clamp((S / 5673.75), 0, 1)
    # Fde.white(F) = (Spectrum(S) - (Median S Value) / (Median S Value) Range(0, 1)
    F = clamp((S - 5673.75) / (5673.75), 0, 1)

    B = Blue(C,K,F)
    G = Green(C,K,F)
    R = Red(C,K,F)
    color = [B,G,R]
    return color


def Color_Note(Note):

    def ntv(note):
        note_map = {'C': 17, 'Do': 17, 'C#': 18, 'Di': 18, 'Db': 18, 'Rah': 18, 'D': 19, 'Re': 19, 'D#': 20, 'Ri': 20, 'Eb': 20, 'Me': 20,
                    'E': 21, 'Mi': 21, 'F': 22, 'Fa': 22, 'F#': 23, 'Fi':23, 'Gb': 23, 'Se': 23, 'G': 24, 'Sol': 24, 'G#': 25, 'Si': 25, 
                    'Ab': 25, 'Le': 25, 'A': 26, 'La':26, 'A#': 27, 'Li': 27, 'Bb':27, 'Te': 27, 'B': 28, 'Ti': 28}

        pitch_class = note[:-1]
        octave = int(note[-1])
        value = (octave - 2) * 12 + note_map[pitch_class]
        return value

    def linear_interpolation_reverse(P, S_points, P_points):
        for i in range(len(P_points) - 1):
            if P_points[i] <= P <= P_points[i + 1]:
                P1, P2 = P_points[i], P_points[i + 1]
                S1, S2 = S_points[i], S_points[i + 1]
                S = S1 + ((P - P1) * (S2 - S1)) / (P2 - P1)
                return S
        return None  # if P is outside the range of P_points
    
    # Example usage with updated sequences:
    S_points = [0,   147, 179, 510, 637.5, 765, 1020, 1530, 1677, 1709, 2040, 2167.5, 2295, 2550, 3060, 3207, 3239, 3570, 3697.5, 3825, 4080, 4590, 4737, 4769, 5100, 5227.5, 5355, 5610, 6120, 6267, 6299, 6630, 6757.5, 6885, 7140, 7650, 7797, 7829, 8160, 8287.5, 8415,  8670, 9180,  9327, 9359, 9690, 9817.5, 9945, 10200, 10710, 10857, 10889, 11220, 11347.5]
    P_points = [3/4, 5/6, 7/8,   1,   9/8, 5/4,  4/3,  3/2,  5/3,  7/4,     2,   9/4,  5/2,  8/3,    3, 10/3,  7/2,    4,    9/2,    5, 16/3,    6, 20/3,    7,    8,      9,   10, 32/3,   12, 40/3,   14,   16,     18,   20, 64/3,   24, 80/3,   28,   32,     36,   40, 128/3,   48, 160/3,   56,   64,     72,   80, 256/3,    96, 320/3,   112,   128,     144]
    #           Sol0  La0  Te0  Do1    Re1  Mi1   Fa1  Sol1   La1   Te1    Do2    Re2   Mi2   Fa2  Sol2   La2   Te2   Do3     Re3   Mi3   Fa3  Sol3   La3   Te3   Do4     Re4   Mi4   Fa4  Sol4   La4   Te4   Do5     Re5   Mi5   Fa5  Sol5   La5   Te5   Do5     Re5   Mi5    Fa5  Sol5    La5   Te5   Do6     Re6   Mi6    Fa6   Sol6    La6    Te6    Do7      Re7
    
    # To find S for a P value in between the given points, say P = 5
    Half_Step_12_Tet = 2**(1/12)
    Do1Value = ntv("C1")
    NoteValue = ntv(Note)
    Half_Steps = NoteValue - Do1Value
    La0 = 27.5 #Hertz
    Do1 = La0*(Half_Step_12_Tet**3) #Hertz
    NoteHertz = Do1*(Half_Step_12_Tet**Half_Steps)
    P = NoteHertz/Do1
    S = linear_interpolation_reverse(P, S_points, P_points)
    
    C = S % 1530
     # ade.black(K) = Spectrum(S) / (Median S Value) Range(0, 1)
    K = clamp((S / 5673.75), 0, 1)
    # Fde.white(F) = (Spectrum(S) - (Median S Value) / (Median S Value) Range(0, 1)
    F = clamp((S - 5673.75) / (5673.75), 0, 1)

    B = Blue(C,K,F)
    G = Green(C,K,F)
    R = Red(C,K,F)
    color = [B,G,R]
    return color

###### Functions ########################################################
# Color_Note()  # input Letter or Solfege, returns BGR
# Color_Hertz() # input Hertz value, returns BGR
# Color_Pitch_Ratio() # input Pitch Ratio, returns BGR
# Color_Length_Ratio() # input String Length Ratio, returns BGR
#########################################################################
###### Example Use ######################################################
#  Creating a circle with a color that is associated with a given note

# diameter = 1200
# radius = int(diameter/2)

# img = np.zeros(shape=(diameter,diameter,3), dtype=np.uint8)


# Using Solfege
# cv2.circle(img,[radius,radius],radius,Color_Note("La4"),-1)

# Using Flat Chromatic Solfege
# cv2.circle(img,[radius,radius],radius,Color_Note("Le4"),-1)

# Using Sharp Chromatic Solfege
# cv2.circle(img,[radius,radius],radius,Color_Note("Li4"),-1)

# Using Letters
# cv2.circle(img,[radius,radius],radius,Color_Note("A4"),-1)

# Using Flat Letters
# cv2.circle(img,[radius,radius],radius,Color_Note("Ab4"),-1)

# Using Sharp Letters
# cv2.circle(img,[radius,radius],radius,Color_Note("A#4"),-1)

# Using Hertz Pitch Value
# cv2.circle(img,[radius,radius],radius,Color_Hertz(440),-1)

# Using Ratio of the interval between two pitches
# cv2.circle(img,[radius,radius],radius,Color_Pitch_Ratio((5/3)*(2**4)),-1)

# Using the String Length Ratio
# cv2.circle(img,[radius,radius],radius,Color_Length_Ratio((3/5)/(2**4),-1)


# cv2.imwrite('Example Color.jpeg',img)

##############################################################################
