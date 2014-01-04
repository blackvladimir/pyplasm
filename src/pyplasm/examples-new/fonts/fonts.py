from pyplasm import *
import os
import xml.dom.minidom

TEXTALIGNMENT = 'centre' #default value
TEXTANGLE = PI / 4 #default value
TEXTWIDTH = 1. #default value
TEXTHEIGHT = 1.0 #default value
FONTWIDTH = 1. #default value
FONTHEIGHT = 1. #default value
FONTSPACING = 0.1 #default value
FONTDEPTH=.5
LINEARAPPROX = 4 #default value

class Character:
    def __init__(self,unicode,xspacing,controlpoints):
        self.xspacing = xspacing
        self.unicode = unicode
        self.controlpoints = controlpoints
class Font:
    def __init__(self,chars,fontsize):
        self.chars = chars
        self.fontsize = fontsize
class Fonts:
    """
    Makes a list of points where cp is a current point and l1 is a list of
    relative points
    """
    def _mkList_(self,l1,cp=None):
        list = []
        #print l1
        for p in l1:
            list.append(self._mkPoint_(p,cp))
        return list
    """
    Makes a point where cp is a current point and p1 is some relative point
    """
    def _mkPoint_(self,p1,cp=None):
        if cp!=None:
            return [p1[0]+cp[0],p1[1]+cp[1]]
        else:
            return [p1[0],p1[1]]

    """
    Reflects a point according to a SVG specifications
    """
    def _reflectPoint_(self,pts):
        p1,p2=pts
        x1,y1=p1
        x2,y2=p2
        x = x2-x1
        y = y2-y1
        p3 = [x2+x,y2+y]
        return p3
    """
    Checks if c char is a path command
    """
    def _isPathCommand_(self,c):
        command_list = [
            'Q','q',
            'T','t',
            'C','c',
            'S','s',
            'L','l',
            'H','h',
            'V','v',
            'M','m',
            'Z','z']
        for com in command_list:
            if com == c:
                return True
        return False

    """
    Parses a string and it returns a list of points
    """
    def _extractPathPoints_(self,pts):
        points = []
        point = []
        number=""
        i=0
        for p in pts:
            if p=='-' or p==' ':
                if number !='' and number!=' ':
                    point.append(float(number))
                if len(point)>1:
                    points.append(point)
                    point = []
                    i=0
                else:
                    i=1
                number = p
            else:
                number +=p
        if number !='' and number !=' ':
            point.append(float(number))
        if point !=[]:
            points.append(point)
        return points

    """
    Parses a path string and it returns a list of commands
    """
    def _parsePathString_(self,pathstring):
        commands = []
        current_command = ""

        for c in pathstring:
            if self._isPathCommand_(c):

                if current_command != "" and current_command != "z" and current_command != "Z":
                    commands.append([current_command,self._extractPathPoints_(control_points)])

                if c=="Z" or c=="z":
                    commands.append([c,None])

                control_points = ""
                current_command = c
            else:
                control_points += c
        return commands

    """
    Parses a list of svg path commands, and it returns a list of Bezier curves which models
    a solid rappresentation of a character
    """
    def _processPathCommands_(self,pathcomands,c=None):
        cpoint = None
        curves = []
        for k in pathcomands:
            key,val = k

            if key == "M" or key == "m":
                last = [val[0][0],val[0][1]]
                first = last
                ctrpts = [last]

            if key =="h" or key=="H":
                if key=="h":
                    next = self._mkPoint_([val[0][0],0],last)
                else:
                    next = self._mkPoint_([val[0][0],0])
                ctrpts = [last,next]
                curves.append(ctrpts)
                last = next

            if key =="v" or key =="V":
                if key=="v":
                    next = self._mkPoint_([0,val[0][0]],last)
                else:
                    next = self._mkPoint_([0,val[0][0]])
                ctrpts = [last,next]
                curves.append(ctrpts)
                last = next

            if key =="l" or key=="L":
                if key=="l":
                    next = self._mkPoint_(val[0],last)
                else:
                    next = self._mkPoint_(val[0])
                ctrpts = [last,next]
                curves.append(ctrpts)
                last = next

            if key == "q" or key == "Q":
                if key == "q":
                    ctrpts = [last] + self._mkList_(val,last)
                else:
                    ctrpts = [last] + val
                cpoint = [ctrpts[-2][0],ctrpts[-2][1]]
                curves.append(ctrpts)
                last = ctrpts[-1]

            if key=="C" or key=="c":
                if key=="c":
                    ctrpts = [last] + self._mkList_(val,last)
                else:
                    ctrpts = [last] + val
                cpoint = [ctrpts[-2][0],ctrpts[-2][1]]
                curves.append(ctrpts)
                last = ctrpts[-1]

            if key == "t" or key == "T":
                if cpoint==None:
                    cpoint = last
                cpoint = self._reflectPoint_([cpoint,last])
                if key == "t":
                    ctrpts = [last,cpoint] + self._mkList_(val,last)
                else:
                    ctrpts = [last,cpoint] + val
                curves.append(ctrpts)
                last = ctrpts[-1]

            if key == "s" or key == "S":
                if cpoint==None:
                    cpoint = last

                cpoint = self._reflectPoint_([cpoint,last])
                if key == "s":
                    ctrpts = [last,cpoint] + self._mkList_(val,last)
                else:
                    ctrpts = [last,cpoint] + val
                curves.append(ctrpts)
                last = ctrpts[-1]

            if key == "z" or key == "Z":
                ctrpts = [first,last]
                curves.append(ctrpts)
                last = []
                first = []
        return curves
    """
    Returns a poliedral rappresentation of a char
    """
    def _mkPol_(self,character,fontsize,dom):
        curves = []
        if len(character.controlpoints)==0:
            return PLASM_T(1)(FONTWIDTH)
        else:
            curves.append(PLASM_S([1,2])([FONTWIDTH/fontsize, FONTHEIGHT/fontsize]))
        for l in character.controlpoints:
            c = PLASM_BEZIER(S1)(l)
            curves.append(MAP(dom, c))
        return PROD([SOLIDIFY(PLASM_STRUCT(curves)), Q(FONTDEPTH)])
        #return STRUCT(curves)

    """
    Parses an svg file and it returns a Font object
    """
    def PARSESVGFONT(self,file):
        if not os.path.exists(file):
            sys.exit("Input file does not exist")
        svg_file = xml.dom.minidom.parse(file)
        svg = svg_file.getElementsByTagName('svg')[0]
        fontface = svg.getElementsByTagName('font-face')
        fontsize=0

        for f in fontface:
            fontsize=float(f.getAttribute("cap-height"))
        font = Font({},fontsize)
        if fontsize!=0:
            glyphs = svg.getElementsByTagName('glyph')
            for g in glyphs:
                unicd = g.getAttribute("unicode")
                xspacing = g.getAttribute("horiz-adv-x")
                if unicd != None and unicd != "":
                    try:
                        charencoded = unicd.encode()
                        pathstring = g.getAttribute("d")
                        pathcommands = self._parsePathString_(pathstring)
                        controlpoints = self._processPathCommands_(pathcommands,charencoded)
                        c = Character(charencoded,xspacing,controlpoints)
                        font.chars[charencoded] = c
                    except:
                        None
        print "finished parsing "+ file +" file..."
        return font

    """
    Aligns chars contained in a word list
    """
    def ALIGNFONT (self,words):
        def ALIGNFONT0 (args2):
            pol1 , pol2, spacing = args2
            box1,box2=(Plasm.limits(pol1),Plasm.limits(pol2))
            vt=Vecf(3)
            for index,pos1,pos2 in [[1, MAX, MIN], [3, MIN, MIN]]:
                    p1=box1.p1 if pos1 is MIN else (box1.p2 if pos1 is MAX else box1.center());p1=p1[index] if index<=p1.dim else 0.0
                    p2=box2.p1 if pos2 is MIN else (box2.p2 if pos2 is MAX else box2.center());p2=p2[index] if index<=p2.dim else 0.0
                    if index==1:
                        sp = spacing
                    else:
                        sp=0.0
                    vt.set(index,vt[index]-(p2-p1-sp))
            return Plasm.Struct([pol1,Plasm.translate(pol2,vt)])
        pols = []
        for w in words:
            if w !=[]:
                pols.append(reduce(lambda x,y: ALIGNFONT0([x,y,FONTSPACING]),w))
            else:
                pols.append([])
        global sp
        sp = 0
        def ALIGNFONT1(x,y):
            global sp
            if y == []:
                sp = sp + FONTWIDTH
                return x
            else:
                oldsp=sp
                sp=0
                return ALIGNFONT0([x,y,FONTWIDTH +oldsp])
        return reduce(lambda x,y: ALIGNFONT1(x,y),pols)
    """
    Returns a list of solid rappresentation of chars that are composing a string
    """
    def CHARPOLS (self,font,dom):
        def CHARPOLS0(charlist):
            string = []
            word = []
            for c in charlist:
                if c==' ':
                    string.append(word)
                    word = []
                else:
                    word.append(self._mkPol_(font.chars[c],font.fontsize,dom))
            if word!=[]:
                string.append(word)
            return string
        return CHARPOLS0
    """
    Returns solid text rappresentation
    """
    def TEXT(self,string,LINEARAPPROX=LINEARAPPROX):
        dom = INTERVALS(1, LINEARAPPROX)
        def TEXT0(font):
            text_fn = COMP([
                self.ALIGNFONT,
                self.CHARPOLS(font,dom),
                CHARSEQ ])
            return text_fn(string)
        return TEXT0
    """
    Returns a solid text rappresentation
    """
    def TEXTWITHATTRIBUTES (self,TEXTALIGNMENT, TEXTANGLE, TEXTWIDTH, TEXTHEIGHT,LINEARAPPROX=LINEARAPPROX):
        def TEXT0(string):
            def TEXT1(font):
                HANDLE = PLASM_STRUCT([PLASM_S([1,2])([TEXTWIDTH/FONTWIDTH, TEXTHEIGHT/FONTHEIGHT]),TEXT(string,LINEARAPPROX)(font)])

                ALIGN = IF([ K(TEXTALIGNMENT == 'centre'),
                    PLASM_T(1)(-PLASM_SIZE(1)(HANDLE)/2),
                    IF([ K(TEXTALIGNMENT == 'right'),
                    PLASM_T(1)(-PLASM_SIZE(1)(HANDLE)) ,ID ])])

                return PLASM_STRUCT([PLASM_R([1,2])(TEXTANGLE), ALIGN, HANDLE])
            return TEXT1
        return TEXT0
    
fonts = Fonts()
TEXT =               fonts.TEXT
TEXTWITHATTRIBUTES = fonts.TEXTWITHATTRIBUTES
PARSESVGFONT =       fonts.PARSESVGFONT
        
