# coding=UTF-8

from scipy import reshape

# for copying objects
import copy

# This is needed to access NCLab's object "nclabinst":
from nclab.engines.python import NCLab
nclabinst = NCLab.instance()

# Import exceptions without traceback:
from nclab.tools import ExceptionWT

#def ExceptionWT(a):
#  print a

# This is needed to measure time:
import time
start = time.clock()
print "Evaluating fenvs.py.."

#default values (see PlasmConfig)
DEFAULT_TOLERANCE=1e-6
DEFAULT_MAX_NUM_SPLIT=10
DEFAULT_USE_OCTREE_PLANES=True

import sys,types,math

# set this to True if you want to do a self test
self_test=False

print __file__

from pyplasm.xge import *

	
#===================================================== 
# Configuration for plasm
#
# EXAMPLE:
# plasm_config.push(<tolerance you want to use::float>)
# <your code>
# plasm_config.pop()
#
#===================================================== 
class PlasmConfig:

	def __init__(self):
		self.stack=[]
		self.push(DEFAULT_TOLERANCE,DEFAULT_MAX_NUM_SPLIT,DEFAULT_USE_OCTREE_PLANES)

	# return actual tolerance
	def tolerance(self):
		return self.stack[-1].tolerance

	# return actual num try
	def maxnumtry(self):
		return self.stack[-1].maxnumtry
		
	def useOctreePlanes(self):
		return self.stack[-1].useoctreeplanes

	# push a config
	def push(self,tolerance,maxnumtry=-1,useoctreeplanes=True):
		class T:pass
		obj=T()
		obj.tolerance=tolerance
		obj.maxnumtry=maxnumtry if maxnumtry>=0 else self.maxnumtry()
		obj.useoctreeplanes=useoctreeplanes
		self.stack+=[obj]

	# pop a config
	def pop(self):
		if len(self.stack)==1:
			raise Exception("Cannot pop the default configuration!")
		self.stack=self.stack[:-1]

plasm_config=PlasmConfig()


#===================================================== 
# Every
#===================================================== 
def every (predicate, iterable):
    for x in iterable:
        if not(predicate(x)):return False
    return True

if self_test: 
	assert(every(lambda x: x>=0,[1,2,3,4]) and not every(lambda x: x>0,[1,-2,3,4]))

#===================================================== 
# from http://www.daniweb.com/code/snippet564.html
#===================================================== 
def curry(fn, *cargs, **ckwargs):
    def call_fn(*fargs, **fkwargs):
        d = ckwargs.copy()
        d.update(fkwargs)
        return fn(*(cargs + fargs), **d)
    return call_fn

def C (fun):
    return lambda arg1: lambda arg2: fun([arg1,arg2])


#===================================================== 
# Define CONStants
#===================================================== 
PI = math.pi
SIN = math.sin
SINH = math.sinh
ASIN = math.asin
COS = math.cos
COSH = math.cosh
ACOS = math.acos
TAN = math.tan

TANH = math.tanh
ATAN = math.atan
ATAN2 = math.atan2
SQRT = math.sqrt
EXP = math.exp
LN = math.log
CEIL = math.ceil
FLOOR = math.floor
ABS = abs
CHAR = chr
ORD = ord
FALSE = False
TRUE = True


def ATAN2(l): 
	return math.atan2(l[1],l[0])


def MOD(l): 
	return float(l[0] % l[1])

# ===================================================== 
# CAT
# =====================================================

def CAT (args):  return reduce(lambda x, y: x + y, args)

if self_test: 
	assert(CAT([[1,2],[3,4]])==[1,2,3,4])



# ===================================================== 
# Matrix inverse
# ===================================================== 

def INV (mat):
    dim=len(mat)
    mat=Matf(CAT(mat)).invert()
    return [ [mat.get(i,j) for j in range(0,dim) ] for i in range(0,dim) ]



if self_test: 
	assert((Matf([1,2,3,4])*Matf(CAT(INV([[1,2],[3,4]]))) ).almostIdentity(0.01))

# ===================================================== 
# AND
# =====================================================
 
def AND (list):
    """ and of all arguments in a list """
    for i in list:
        if not(i):return False
    return True



if self_test: 
	assert(AND([True,True])==True and AND([True,False])==False)

#===================================================== 
# hpc type
#===================================================== 

pol_type = Hpc

def is_polyhedra_complex (obj):
    return isinstance(obj, pol_type)

def ISPOL (obj):
    return isinstance(obj, pol_type)

if self_test: 
	assert(ISPOL(Plasm.cube(2))==True)

#===================================================== 
# FL IDentity Function 
#===================================================== 

def ID (anyValue):
    """IDentity function. For any argument retruns the argument"""
    return anyValue

if self_test: 
	assert(ID(True)==True)


#===================================================== 
# FL CONStant Function 
#===================================================== 

def K(AnyValue):
    def K0 (obj): return AnyValue
    return K0



TT = K(TRUE)

if self_test: 
	assert(K(1)(2)==1)

# ===================================================
# DISTL
# ===================================================

def DISTL(args):
    Element, List = args
    return [ [Element, e] for e in List ]
    


if self_test: 
	assert(DISTL([1,[2,3,4]])==[[1,2],[1,3],[1,4]])

# ===================================================
# DISTR
# ===================================================

def DISTR(args):
    List, Element = args
    return [ [e,Element] for e in List ]



if self_test: 
	assert(DISTR([[1,2,3],0])==[[1,0],[2,0],[3,0]])


# ===================================================
# Composition
# ===================================================

def COMP(Funs):
   def compose(f,g):
      def h(x): return f(g(x))
      return h
   return reduce(compose,Funs)



if self_test: 
	assert(COMP([lambda x: x+[3],lambda x: x+[2],lambda x: x+[1]])([0])==[0,1,2,3])


# ===================================================
# Apply-to-all 
# ===================================================

def AA (f):
    def AA0 (args): return map(f, args)
    return AA0



if self_test: 
	assert(AA(lambda x: x*2)([1,2,3])==[2,4,6])



# ===================================================
# PLASM  Comparison operators 
# ===================================================

def Eq (x,y): return x == y

def EQ(List):
    for i in List:
       if not i==List[0]: return False
    return True

def NEQ(List): 
    return not EQ(List)


if self_test: 
	assert(EQ([1,1,1]) and not EQ([1,1,2]))
	assert(NEQ([1,1,2])==True and NEQ([1,1,2/2])==False)

def LT (a):return lambda b: b<a
def LE (a):return lambda b: b<=a
def GT (a):return lambda b: b>a
def GE (a):return lambda b: b>=a

if self_test: assert(LT(2)(1) and LE(2)(2) and  GT(2)(3) and  GE(2)(2))

def ISGT (args):A , B = args;return GT(A)(B)
def ISLT (args):A , B = args;return LT(A)(B)
def ISGE (args):A , B = args;return GE(A)(B)
def ISLE (args):A , B = args;return LE(A)(B)


def BIGGER (args): 
	A , B = args
	return A if A>=B else B

def SMALLER (args):
	A , B = args
	return A if A<=B else B


# ===================================================
# FILTER
# ===================================================

def FILTER(predicate):
	def FILTER0(sequence):
		ret=[]
		for item in sequence:
			if predicate(item): ret+=[item]
		return ret
	return FILTER0

if self_test:
	assert FILTER(LE(0))([-1,0,1,2,3,4])==[-1,0]
	assert FILTER(GE(0))([-1,0,1,2,3,4])==[0,1,2,3,4]


# ===================================================
# Apply 
# ===================================================

def APPLY(args):
    f,x = args
    return apply(f,[x])



if self_test: 
	assert(APPLY([lambda x:x*2,2])==4)

# ===================================================
# INSR
# ===================================================

def PLASM_INSR(f):
    def INSR0(seq):
        length=len(seq)
        res = seq[-1]
        for i in range(length - 2,-1,-1): res = f([seq[i], res])
        return res
    return INSR0 

  

if self_test: 
	assert(PLASM_INSR(lambda x: x[0]-x[1])([1,2,3])==2)

# ===================================================
# INSL
# ===================================================
def INSL(f):
    def INSL0 (seq):
        res = seq[0]
        for item in seq[1:]: res = f([res,item])
        return res
    return INSL0   

   

if self_test: 
	assert(INSL(lambda x: x[0]-x[1])([1,2,3])==-4) 


# ===================================================
# CONS
# ===================================================

def CONS (Funs): return lambda x : [f(x) for f in Funs]



if self_test: 
	assert(CONS( [lambda x : x+1,lambda x : x+2])(0)==[1,2])



# ===================================================
# IF THEN ELSE purely functional 
# ===================================================

def IF (funs):
    def IF1 (arg):
        f1, f2, f3 = funs
        return f2(arg) if f1(arg) else f3(arg)
    return IF1
        
 

if self_test: 
	assert(IF([lambda x: x, K(True),K(False)])(True)==True)
	assert(IF([lambda x: x, K(True),K(False)])(False)==False)



# ===================================================
# FL LIFT and RAISE functions 
# ===================================================

def LIFT (f):
    return lambda funs: COMP([f, CONS(funs)])


def RAISE (f):
    def RAISE0 (args):
        return IF([ISSEQOF(ISFUN), LIFT(f), f])(args)
    return RAISE0



# ===================================================
# PLASM  predicates 
# ===================================================

def ISNUM (x): 
	return  isinstance(x, int) or isinstance(x, long) or  isinstance(x, float) or  isinstance(x, complex) or (sys.platform=='cli' and type(x) == System.Single)
		
		
if self_test: 
	assert(ISNUM(0.0))

def NUMBER_FROM_ZERO_TO_ONE_P (x):  return  ISNUM(x) and x >= 0 and x <= 1

def ISFUN (x): return callable(x)

if self_test: 
	assert(ISFUN(lambda x:x) and ISFUN(abs) and not ISFUN(3))

def ISNUMPOS (x): return ISNUM(x) and x > 0
def ISNUMNEG (x): return ISNUM(x) and x < 0
def ISINT (x): return isinstance(x,int)
def ISLONG (x): return isinstance(x,long)
def ISINTPOS (x): return isinstance(x,int) and x > 0
def ISINTNEG (x): return isinstance(x,int) and x < 0
def ISREAL (x): return isinstance(x,float)
def ISREALPOS (x): return isinstance(x,float) and x > 0
def ISREALNEG (x): return isinstance(x,float) and x < 0
def ISCOMPLEX (x): return isinstance(x,complex)
def ISSEQ (x): return isinstance(x,list)
def ISSEQ_NOT_VOID (x): return True if (isinstance(x,list) and (len(x) >= 1)) else False

def ISSEQOF (type_checker):
    def ISSEQOF0 (arg):
        if not isinstance(arg, list): return False
        for item in arg:
           if not type_checker(item): return False
        return True
    return ISSEQOF0

if self_test: 
	assert(ISSEQOF(lambda x: isinstance(x,int))([1,2,3])==True)
	assert(ISSEQOF(lambda x: isinstance(x,int))([1,2,3.0])==False)

def ISNULL (x): return isinstance(x,list) and len(x) == 0
def ISBOOL (x): return isinstance(x,bool)
def ISPAIR (x): return isinstance(x,list) and len(x) == 2
def ISCHAR (x): return isinstance(x,str) and len(x) == 1
def ISSTRING (x): return isinstance(x,str)
def ISMAT(x): return  isinstance(x, list) and AND([isinstance(e,list) for e in x])
def ISEVEN (N): return isinstance(N,int) and (N%2)==1
def ISNAT(N): return isinstance(N,int) and N>=0
def ISZERO(N): return N==0
def ISODD(N): return not ISEVEN(N)

if self_test: 
	assert(ISMAT([[1,2],[3,4]])==True and not ISMAT([1,2,3,4]))

def VECTSUM(vects):  return map(sum,zip(*vects))
def VECTDIFF(vects): return map(lambda l: l[0]-sum(l[1:]),zip(*vects))

if self_test: 
	assert(VECTDIFF([[10,11,12],[0,1,2],[1,1,1]])==[9,9,9])
	assert(VECTSUM([[10,11,12],[0,1,2],[1,1,1]])==[11,13,15])

def IS_PLASM_POINT_2D (obj): 
	return isinstance(obj, list) and (len(obj) == 2) 


# ===================================================
# MEANPOINT
# ===================================================

def MEANPOINT (points):
	coeff=1.0/len(points)
	return map(lambda x:coeff*x,VECTSUM(points))


if self_test:
	assert MEANPOINT([[0,0,0],[1,1,1],[2,2,2]])==[1,1,1]

# ===================================================
# n-ary addition
# ===================================================

def PLASM_SUM(args):


	if isinstance(args,list) and ISPOL(args[0]): 
		return PLASM_UNION(args)
	
	if isinstance(args,list) and ISNUM(args[0]): 
		return sum(args)

	if isinstance(args,list) and isinstance((args[0]),list): 

		#matrix sum
		if isinstance(args[0][0],list):
			return AA(VECTSUM)(zip(*args))

		# vector sum
		else:
			return VECTSUM(args)

	raise Exception("\'+\' function has been applied to %s!" % repr(args))        


PLASM_ADD = PLASM_SUM

if self_test: 
	assert(ADD([1,2,3])==6 and ADD([[1,2,3],[4,5,6]])==[5,7,9])
	assert PLASM_SUM([ [[1,2],[3,4]],  [[10,20],[30,40]],  [[100,200],[300,400]] ])==[[111,222],[333,444]]
	assert(LIFT(ADD)([math.cos,math.sin])(PI/2)==1.0)
	assert(RAISE(ADD)([1,2])==3)
	assert(RAISE(ADD)([math.cos,math.sin])(PI/2)==1.0)





# ===================================================
# n-ary DIFFerence 
# ===================================================

def PLASM_NDIFF(args):

	if isinstance(args,list) and ISPOL(args[0]): 
		return  PLASM_DIFFERENCE(args)

	if ISNUM(args): 
		return -1 * args

	if isinstance(args,list) and  ISNUM(args[0]): 
			return reduce(lambda x,y: x - y, args)

	if isinstance(args,list) and  isinstance(args[0],list): 

		#matrix difference
		if isinstance(args[0][0],list):
			return AA(VECTDIFF)(zip(*args))

		# vector diff
		else:
			return VECTDIFF(args)
	
	raise Exception("\'-\' function has been applied to %s!" % repr(args))     



if self_test: 
	assert( PLASM_DIFF(2)==-2 and  PLASM_DIFF([1,2,3])==-4 and  PLASM_DIFF([[1,2,3],[1,2,3]])==[0,0,0])

# ===================================================
# n-ary PRODuct 
# ===================================================

def PLASM_PROD(args):        
    if isinstance(args,list) and ISPOL(args[0]): return  PLASM_POWER(args)
    if isinstance(args,list) and ISSEQOF(ISNUM)(args): return reduce(lambda x,y: x * y, args)
    if isinstance(args,list) and len(args) == 2 and ISSEQOF(ISNUM)(args[0]) and ISSEQOF(ISNUM)(args[1]): return  Vecf(args[0])*Vecf(args[1])
    raise Exception("PLASM_PROD function has been applied to %s!" % repr(args))



if self_test: 
	assert(PLASM_PROD([1,2,3,4])==24 and PLASM_PROD([[1,2,3],[4,5,6]])==32)

SQR = RAISE(RAISE(PLASM_PROD))([ID,ID])


# ===================================================
# n-ary DIVision 
# ===================================================

def DIV(args):
    return reduce(lambda x,y: x/float(y), args)


if self_test: 
	assert(DIV([10,2,5])==1.0)

# ===================================================
# REVERSE
# ===================================================

def REVERSE(List): 
   ret=[x for x in List]
   ret.reverse()
   return ret



if self_test: 
	assert(REVERSE([1,2,3])==[3,2,1] and REVERSE([1])==[1] )

LEN = len


# ===================================================
# TRANS
# ===================================================

def TRANS (List): 
	return map(list, zip(*List))


if self_test: 
	assert(TRANS([[1,2],[3,4]])==[[1,3],[2,4]])

def FIRST (List): return List[0]
def LAST (List): return List[-1]
def TAIL (List): return List[1:]
def RTAIL (List): return List[:-1]
def AR (args): return args[0] + [args[-1]]
def AL (args): return [args[0]] + args[-1]
def LIST(x): return [x]


if self_test: 
	assert(AR([ [1,2,3],0,])==[1,2,3,0])

if self_test: 
	assert(AL([ 0,[1,2,3]])==[0,1,2,3])


# ===================================================
# FL CONStruction 
# ===================================================

greater=max
BIGGEST=max
SMALLEST = min


if self_test: 
	assert(greater(1,2)==2 and BIGGEST([1,2,3,4])==4)
	

# ===================================================
# PLASM  logical operators 
# ===================================================

And=all
AND=And 
Or=any
OR=Or

def Not(x): 
	return not x

NOT = AA(Not) 

if self_test: 
	assert(AND ([True,True,True])==True and AND ([True,False,True])==False)
	assert(OR ([True,False,True])==True and OR ([False,False,False])==False)


# ===================================================
# PROGRESSIVESUM
# ===================================================

def PROGRESSIVESUM(arg):
	ret,acc=[],0
	for value in arg:
		acc+=value
		ret+=[acc]
	return ret



if self_test:
	assert PROGRESSIVESUM([1,2,3,4])==[1,3,6,10]

# ===================================================
# PLASM range builders 
# ===================================================

def INTSTO (n): 
    return range(1,n+1)


if self_test: 
	assert(INTSTO(5)==[1,2,3,4,5])


def FROMTO (args):   
    return range(args[0],args[-1]+1)


if self_test: 
	assert(FROMTO ([1,4])==[1,2,3,4])

# ===================================================
# PLASM  selectors
# ===================================================

def SEL (n): 
    return lambda lista: lista[int(n)-1]


S1 = SEL(1)
S2 = SEL(2)
S3 = SEL(3)
S4 = SEL(4)
S5 = SEL(5)
S6 = SEL(6)
S7 = SEL(7)
S8 = SEL(8)
S9 = SEL(9)
S10 = SEL(10)

if self_test: 
	assert(S1([1,2,3])==1 and S2([1,2,3])==2)

# ===================================================
# PLASM  repeat operators 
# ===================================================

def N (n): 
    """
    N: Standard core of PyPLaSM
    repetition operator. Returns the sequence with n repetitions of arg
    (n::isintpos)(arg::tt) -> (isseq)
    """
    return lambda List: [List]*int(n)


if self_test: 
	assert(N(3)(10)==[10,10,10])

def DIESIS (n): 
    """
    N: Standard core of PyPLaSM
    repetition operator. Returns the sequence with n repetitions of arg
    (n::isintpos)(arg::tt) -> (isseq)
    """
    return lambda List: [List]*int(n)


if self_test: 
	assert(DIESIS(3)(10)==[10,10,10])

def NN (n): 
    """
    NN:   Standard core of PyPLaSM
    sequence repetition operator. Returns the sequence CAT(N(seq))
    (n::isintpos)(seq::tt) -> (isseq)
    """
    return lambda List: List*int(n)


if self_test: 
	assert(NN (3)([10])==[10,10,10])


def DOUBLE_DIESIS (n): 
    """
    NN:   Standard core of PyPLaSM
    sequence repetition operator. Returns the sequence CAT(N(seq))
    (n::isintpos)(seq::tt) -> (isseq)
    """
    return lambda List: List*int(n)

# NEW DEFINITION:
def REPEAT(n, args):
    return DOUBLE_DIESIS(n)(args)

if self_test: 
	assert(DOUBLE_DIESIS  (3)([10])==[10,10,10])



# ===================================================
# Curryfing function 
# ===================================================

def C (fun):
    return lambda arg1: lambda arg2: fun([arg1,arg2])

# ===================================================
# Miscellanea (1/3) of "standard" functions 
# ===================================================

def AS(fun):
    return lambda args: COMP([CONS, AA(fun)])(args)


if self_test: assert(AS(SEL)([1,2,3])([10,11,12])==[10,11,12])

def AC(fun):
    return lambda args: COMP(AA(fun)(args))


if self_test: assert(AC(SEL)([1,2,3])([10,11,[12,[13]]])==13)

def CHARSEQ (String):
    return [String[i] for i in range(len(String))]

if self_test: assert(CHARSEQ('hello')==['h','e','l','l','o'])

def STRING (Charseq): return reduce(lambda x,y: x+y,Charseq)

if self_test: 
	assert(STRING(CHARSEQ('hello'))=='hello')

def RANGE (Pair):
    if ( (Pair[-1]-Pair[0]) >= 0 ): return range(Pair[0], Pair[-1] + 1)
    return range(Pair[0], Pair[-1] - 1, -1)



if self_test: 
	assert(RANGE ([1,3])==[1,2,3] and RANGE ([3,1])==[3,2,1])

def SIGN (Number): return +1 if Number>=0 else -1

if self_test: assert(SIGN(10)==1 and SIGN(-10)==-1)

def PRINT (AnyValue):
    print(AnyValue)
    return AnyValue


def PRINTPOL (PolValue):
    Plasm.Print(PolValue)
    sys.stdout.flush()
    return PolValue



# ===================================================
# TREE
# ===================================================

def TREE (f):
    def TREE_NO_CURRIED (fun,List):
        length = len(List)
        if length == 1: return List[0]
        k = int(len(List)/2)
        return f([TREE_NO_CURRIED(f, List[:k])] + [TREE_NO_CURRIED(f, List[k:])])
    return lambda x: TREE_NO_CURRIED(f,x)
    

if self_test: 
	assert(TREE(lambda x: x[0] if x[0]>=x[-1] else x[-1])([1,2,3,4,3,2,1])==4)
	assert(TREE(lambda x: x[0] if x[0]>=x[-1] else x[-1])([1,2,3,4,3,2])==4)

# ===================================================
# MERGE
# ===================================================

def MERGE (f):
    def MERGE_NO_CURRIED (f, List):
        list_a, list_b = List
        if len(list_a) == 0: return list_b
        if len(list_b) == 0: return list_a
        res = f(list_a[0], list_b[0])
        if not(res):
            return [list_a[0]] + MERGE_NO_CURRIED(f,[list_a[1:], list_b])
        else:
            return [list_b[0]] + MERGE_NO_CURRIED(f,[list_a, list_b[1:]])
    return lambda x: MERGE_NO_CURRIED(f,x)

if self_test: 
	assert(MERGE(lambda x,y:x>y)([[1,3,4,5],[2,4,8]])==[1,2,3,4,4,5,8])

# ===================================================
# CASE
# ===================================================

def CASE (ListPredFuns):
    def CASE_NO_CURRIED (ListPredFuns, x):
        for p in ListPredFuns:
           if p[0](x): return p[1](x)
    return lambda arg: CASE_NO_CURRIED(ListPredFuns, arg)

if self_test: 
	assert(CASE([[LT(0),K(-1)],[C(EQ)(0),K(0)],[GT(0),K(+1)]])(-10)==-1)
	assert(CASE([[LT(0),K(-1)],[C(EQ)(0),K(0)],[GT(0),K(+1)]])(   0)==0)
	assert(CASE([[LT(0),K(-1)],[C(EQ)(0),K(0)],[GT(0),K(+1)]])(10)==+1)

# ===================================================
# GEOMETRIC FUNCTION 
# ===================================================

# THIS was originally VIEW() but we need to 
# redefine it below.
def PLASM_VIEW (obj, Background = True):
    if self_test: Background = False
    Plasm.View(obj, Background) 
    return obj
def VIEWBASE(objects):
    geoms = []
    for x in objects:
        geoms.append(x.geom)
    nclabinst.visualize(nclabinst.converter(geoms))

# English:
def VIEW(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence == 0): raise ExceptionWT("The VIEW(...) command must contain at least one object!")
    VIEWBASE(sequence)
def V(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence == 0): raise ExceptionWT("The V(...) command must contain at least one object!")
    VIEWBASE(sequence)
def SHOW(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("The SHOW(...) command must contain at least one object!")
    VIEWBASE(sequence)
# Czech:
def UKAZ(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Příkaz UKAZ(...) musí obsahovat alespoň jeden objekt!")
    VIEWBASE(sequence)
def ZOBRAZ(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Příkaz ZOBRAZ(...) musí obsahovat alespoň jeden objekt!")
    VIEWBASE(sequence)
# Polish:
def ZOBACZ(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Poleceń ZOBACZ(...) musi zawierać co najmniej jeden obiekt!")
    VIEWBASE(sequence)
def POKAZ(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Poleceń POKAZ(...) musi zawierać co najmniej jeden obiekt!")
    VIEWBASE(sequence)
# German:
def ZEIGE(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Der Befehl ZEIGE(...) muss mindestens ein Objekt enthalten!")
    VIEWBASE(sequence)
def ANSICHT(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Der Befehl ANSICHT(...) muss mindestens ein Objekt enthalten!")
    VIEWBASE(sequence)
# Spanish:
def MOSTRAR(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("El comando MOSTRAR(...) debe contener al menos un objeto!")
    VIEWBASE(sequence)
def MUESTRA(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("El comando MUESTRA(...) debe contener al menos un objeto!")
    VIEWBASE(sequence)
# Italian:
def MOSTRARE(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Il comando MOSTRARE(...) deve contenere almeno un oggetto!")
    VIEWBASE(sequence)
def MOSTRA(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("Il comando MOSTRA(...) deve contenere almeno un oggetto!")
    VIEWBASE(sequence)
# French:
def MONTRER(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("La commande MONTRER(...) doit contenir au moins un objet!")
    VIEWBASE(sequence)
def MONTRE(*args):
    sequence = flatten(*args)
    for obj in sequence:
        if SIZEX(obj) == 0 and SIZEY(obj) == 0 and SIZEZ(obj) == 0:
            raise ExceptionWT("One of the objects that you are trying to display is empty!")
    if len(sequence) == 0: raise ExceptionWT("La commande MONTRE(...) doit contenir au moins un objet!")
    VIEWBASE(sequence)

# ===================================================
# BASE OBJECT
# ===================================================

class BASEOBJ:
    def __init__(self, basegeom):
        self.color = [200, 200, 200]
        self.geom = basegeom
        self.dim = PLASM_DIM(basegeom)
        self.material = [1,0,0,1,  0,1,0,1,  0,0,1,0, 0,0,0,1, 100]
    def setmaterial(self, mat):
        # Check if the material is a list:
        if type(mat) is list:
            if len(mat) != 17:
                raise ExceptionWT("Material must be a list of 17 values: ambientRGBA, diffuseRGBA specularRGBA emissionRGBA shininess")
            else:
                self.material = mat
                self.geom = PLASM_MATERIAL(mat)(self.geom)
        else:
            raise ExceptionWT("Material must be a list of 17 values: ambientRGBA, diffuseRGBA specularRGBA emissionRGBA shininess")
    def getmaterial():
        return self.material
    def setcolor(self, color = [200, 200, 200]):
        # Check if the color is a list:
        if type(color) is list:
          # Sanity checks:
          if len(color) <> 3 and len(color) <> 4:
            raise ExceptionWT("Color must be a list of length 3 (R, G, B) or 4 (R, G, B, A)!")
          if color[0] < 0 or color[0] > 255 or color[1] < 0 or color[1] > 255 or color[2] < 0 or color[2] > 255:
            raise ExceptionWT("RGB values in color definition must lie between 0 and 255!")
          if len(color) == 4:
            if color[3] < 0 or color[3] > 1:
              raise ExceptionWT("Opacity value in color definition must be between 0 and 1!")
        else: 
            raise ExceptionWT("Color must be a list, either [R, G, B] or [R, G, B, A]!")
        self.color = color
	self.geom = PLASM_COLOR(color)(self.geom)
    def getcolor(self):
        return self.color
    def move(self, t1, t2, t3 = 0):
        if t3 == 0:
            self.geom = PLASM_TRANSLATE([1, 2])([t1, t2])(self.geom)
        else:
            if self.dim <> 3:
                raise ExceptionWT("2D objects may be moved in the xy-plane only, not in 3D!")
            self.geom = PLASM_TRANSLATE([1, 2, 3])([t1, t2, t3])(self.geom)
        self.setcolor(self.color)
    def rotaterad(self, angle_rad, axis = 3, point = [0, 0, 0]):
        # this is a bit nasty but it allows to give center point without the axis in 2D:
        centerpoint = point
        if self.dim == 2 and isinstance(axis, list):
            centerpoint = axis
            axis = 3
        # check the axis:
        if axis != 1 and axis != 2 and axis != 3: 
            raise ExceptionWT("The third argument of ROTATE must be either 1 (x-axis), 2 (y-axis), or 3 (z-axis)!")
	if self.dim == 2 and axis <> 3:
            raise ExceptionWT("2D objects may be rotated in the xy-plane only, not in 3D!")
        if axis == 1: plane_indexes = [2, 3]
        elif axis == 2: plane_indexes = [1, 3]
        else: plane_indexes = [1, 2]
        # sanity check for the center point:
        if not isinstance(centerpoint, list):
            raise ExceptionWT("The optional center point in ROTATE must be a list!")
        centerpointdim = len(centerpoint)
        if centerpointdim != 2 and centerpointdim != 3:
            raise ExceptionWT("The optional center point in ROTATE must be a list of either 2 or 3 coordinates!")
        # if 3D object and 2D point, make third coordinate zero:
        if centerpointdim == 2 and self.dim == 3:
            centerpoint.append(0)
        # if 2D object and 3D point, ignore third coordinate:
        if centerpointdim == 3 and self.dim == 2:
            forgetlast = centerpoint.pop()        
        # if point is not zero, move object first:
        if self.dim == 2:
            if centerpoint[0] != 0 or centerpoint[1] != 0:
                self.geom = PLASM_TRANSLATE([1, 2])([-centerpoint[0], -centerpoint[1]])(self.geom)   
        else:
            if centerpoint[0] != 0 or centerpoint[1] != 0 or centerpoint[2] != 0:
                self.geom = PLASM_TRANSLATE([1, 2, 3])([-centerpoint[0], -centerpoint[1], -centerpoint[2]])(self.geom)  
        # call the PLaSM rotate command:
        dim = max(plane_indexes)
	self.geom = Plasm.rotate(self.geom, dim, plane_indexes[0], plane_indexes[1], angle_rad)
        # if point is not zero, return object back:
        if self.dim == 2:
            if centerpoint[0] != 0 or centerpoint[1] != 0:
                self.geom = PLASM_TRANSLATE([1, 2])([centerpoint[0], centerpoint[1]])(self.geom)   
        else:
            if centerpoint[0] != 0 or centerpoint[1] != 0 or centerpoint[2] != 0:
                self.geom = PLASM_TRANSLATE([1, 2, 3])([centerpoint[0], centerpoint[1], centerpoint[2]])(self.geom)
        # return color:
        self.setcolor(self.color)
    def rotate(self, angle_deg, axis = 3, point = [0, 0, 0]):
        angle_rad = PI * angle_deg / 180.
        self.rotaterad(angle_rad, axis, point)
        self.setcolor(self.color)
    def getdimension(self):
        return self.dim
    def rotaterel(self, angle_deg, axis = 3):
        if axis != 1 and axis != 2 and axis != 3: 
          raise ExceptionWT("The third argument of the command ROTATE must be either 1 (x-axis), 2 (y-axis), or 3 (z-axis)!")
	if self.dim == 2 and axis <> 3:
            raise ExceptionWT("2D objects may be rotated in the xy-plane only, not in 3D!")
        if self.dim != 2 and self.dim != 3:
           raise ExceptionWT("Error in ROTATE: Object dimension must be either 2 or 3.")
        if self.dim == 2:
          x = 0.5 * (self.minx() + self.maxx())
          y = 0.5 * (self.miny() + self.maxy())
          self.move(-x, -y)
          self.rotate(angle_deg, axis)
          self.move(x, y)
        else:
          x = 0.5 * (self.minx() + self.maxx())
          y = 0.5 * (self.miny() + self.maxy())
          z = 0.5 * (self.minz() + self.maxz())
          self.move(-x, -y, -z)
          self.rotate(angle_deg, axis)
          self.move(x, y, z)
        self.setcolor(self.color)
    def scale(self, a, b, c = 1.0):
        if a <= 0 or b <= 0 or c <= 0:
            raise ExceptionWT("When scaling an object, all axial coefficients must be greater than zero!")
	if self.dim == 2 and c <> 1.0:
            raise ExceptionWT("2D objects may be scaled in the xy-plane only, not in 3D!")
        self.geom = PLASM_SCALE([1, 2, 3])([a, b, c])(self.geom)
        self.setcolor(self.color)
    def minx(self):
        return MIN(1)(self.geom)
    def miny(self):
        return MIN(2)(self.geom)
    def minz(self):
        return MIN(3)(self.geom)
    def maxx(self):
        return MAX(1)(self.geom)
    def maxy(self):
        return MAX(2)(self.geom)
    def maxz(self):
        return MAX(3)(self.geom)
    def sizex(self):
        return MAX(1)(self.geom) - MIN(1)(self.geom)
    def sizey(self):
        return MAX(2)(self.geom) - MIN(2)(self.geom)
    def sizez(self):
        return MAX(3)(self.geom) - MIN(3)(self.geom)
    def erasex(self, erasexmin, erasexmax):
        minx = self.minx()
        maxx = self.maxx()
        miny = self.miny()
        maxy = self.maxy()        
        if self.dim == 2:
            box = BOX(erasexmax - erasexmin, self.maxy() - self.miny() + 2)
            MOVE(box, erasexmin, self.miny() - 1)
    	    self.geom = PLASM_DIFF([self.geom, box.geom])
            self.setcolor(self.color)
        else:
            minz = self.minz()
            maxz = self.maxz()
            box = BOX(erasexmax - erasexmin, self.maxy() - self.miny() + 2, self.maxz() - self.minz() + 2)
            MOVE(box, erasexmin, self.miny() - 1, self.minz() - 1)
    	    self.geom = PLASM_DIFF([self.geom, box.geom])
            self.setcolor(self.color)
    def splitx(self, coord):
        minx = self.minx()
        maxx = self.maxx()
        miny = self.miny()
        maxy = self.maxy()        
        if self.dim == 2:
            box1 = BOX(coord - minx, self.maxy() - self.miny() + 2)
            box2 = BOX(maxx - coord, self.maxy() - self.miny() + 2)
            MOVE(box1, minx, self.miny() - 1)
            MOVE(box2, coord, self.miny() - 1)
    	    obj1 = BASEOBJ(PLASM_INTERSECTION([self.geom, box1.geom]))
    	    obj2 = BASEOBJ(PLASM_INTERSECTION([self.geom, box2.geom]))
            obj1.setcolor(self.color)
            obj2.setcolor(self.color)
        else:
            minz = self.minz()
            maxz = self.maxz()
            box1 = BOX(coord - minx, self.maxy() - self.miny() + 2, self.maxz() - self.minz() + 2)
            box2 = BOX(maxx - coord, self.maxy() - self.miny() + 2, self.maxz() - self.minz() + 2)
            MOVE(box1, minx, self.miny() - 1, self.minz() - 1)
            MOVE(box2, coord, self.miny() - 1, self.minz() - 1)
    	    obj1 = BASEOBJ(PLASM_INTERSECTION([self.geom, box1.geom]))
    	    obj2 = BASEOBJ(PLASM_INTERSECTION([self.geom, box2.geom]))
            obj1.setcolor(self.color)
            obj2.setcolor(self.color)
        return obj1, obj2

# ===================
# SIZEX, SIZEY, SIZEZ
# ===================

def SIZEX(obj):
    return obj.sizex()

def SIZEY(obj):
    return obj.sizey()

def SIZEZ(obj):
    return obj.sizez()

# ===========================================================
# ERASE(obj, axis, min, max) - ERASE PART OF OBJECT THAT LIES 
# BETWEEN MIN AND MAX in AXIAL DIRECTION "axis"
# ===========================================================

def ERASE(obj, axis, minval, maxval):
    if axis != 1 and axis != 2 and axis != 3:
        raise ExceptionWT("In ERASE(obj, axis, minval, maxval), axis must be 1 (x-axis), 2 (y-axis) or 3 (z-axis)!")
    if maxval <= minval:
        raise ExceptionWT("In ERASE(obj, axis, minval, maxval), minval must be less than maxval!")
  
    if not isinstance(obj, list):
        if axis == 1:
            obj.erasex(minval, maxval)
        if axis == 2:
            obj.rotate(-90, 3)
            obj.erasex(minval, maxval)
            obj.rotate(90, 3)
        if axis == 3:
            if obj.dim == 2:
                 raise ExceptionWT("In ERASE(obj, axis, minval, maxval), axis = 3 may not be used with 2D objects!")
            obj.rotate(-90, 2)
            obj.erasex(minval, maxval)
            obj.rotate(90, 2)
    else:
        obj = flatten(obj) # flatten the rest as there may be structs
        for oo in obj:
            if axis == 1:
                oo.erasex(minval, maxval)
            if axis == 2:
                oo.rotate(-90, 3)
                oo.erasex(minval, maxval)
                oo.rotate(90, 3)
            if axis == 3:
                if oo.dim == 2:
                    raise ExceptionWT("In ERASE(obj, axis, minval, maxval), axis = 3 may not be used with 2D objects!")
                oo.rotate(-90, 2)
                oo.erasex(minval, maxval)
                oo.rotate(90, 2)
    return COPY(obj)

# ============================================================
# SPLIT(obj, axis, coord) - SPLIT AN OBJECT IN AXIAL DIRECTION 
# "axis" INTO TWO PARTS SEPARATED AT COORDINATE "coord"
# ============================================================

def SPLIT(obj, axis, coord):
    if axis != 1 and axis != 2 and axis != 3:
        raise ExceptionWT("In SPLIT(obj, axis, coord), axis must be 1 (x-axis), 2 (y-axis) or 3 (z-axis)!")
  
    if not isinstance(obj, list):
        if axis == 1:
            obj1, obj2 = obj.splitx(coord)
        if axis == 2:
            obj.rotate(-90, 3)
            obj1, obj2 = obj.splitx(coord)
            obj1.rotate(90, 3)
            obj2.rotate(90, 3)
        if axis == 3:
            if obj.dim == 2:
                 raise ExceptionWT("In SPLIT(obj, axis, coord), axis = 3 may not be used with 2D objects!")
            obj.rotate(-90, 2)
            obj1, obj2 = obj.splitx(coord)
            obj1.rotate(90, 2)
            obj2.rotate(90, 2)
    else:
        obj = flatten(obj) # flatten the rest as there may be structs
        obj1 = []
        obj2 = []
        for oo in obj:
            if axis == 1:
                oo1, oo2 = oo.splitx(coord)
            if axis == 2:
                oo.rotate(-90, 3)
                oo1, oo2 = oo.splitx(coord)
                oo1.rotate(90, 3)
                oo2.rotate(90, 3)
            if axis == 3:
                if oo.dim == 2:
                    raise ExceptionWT("In SPLIT(obj, axis, coord), axis = 3 may not be used with 2D objects!")
                oo.rotate(-90, 2)
                oo1, oo2 = oo.splitx(coord)
                oo1.rotate(90, 2)
                oo2.rotate(90, 2)
            obj1.append(oo1)
            obj2.append(oo2)
    return obj1, obj2

# =========================================================
# COPYING OBJECTS AND LISTS OF OBJECTS (LISTS ARE FLATTENED
# =========================================================

def COPY(obj):
    if not isinstance(obj, list):
        return copy.copy(obj)
    else:
        obj1 = flatten(obj) # flatten the rest as there may be structs
        newlist = []
        for x in obj1:
            newlist.append(copy.copy(x))
        return newlist

# Czech:
KOPIE = COPY
# Polish:
KOPIA = COPY
# German:
# Like Czech
# Spanish:
# Italian:
COPIA = COPY
# French:
COPIE = COPY

# ===================================================
# CUBOID
# ===================================================

def CUBOID (sizes_list):
    dim = len(sizes_list)
    pol = Plasm.scale(Plasm.cube(dim), Vecf([0.0] + sizes_list))
    return pol

if self_test: 
	assert(Plasm.limits(CUBOID([1,2,3]))==Boxf(Vecf(1,0,0,0),Vecf(1,1,2,3)))

# ===================================================
# CUBE
# ===================================================

def CUBE(size):
    if size <= 0: 
        raise ExceptionWT("CUBE(x) requires a positive value of x!")
    return BASEOBJ(CUBOID([size, size, size]))
# English:
# Czech:
KRYCHLE = CUBE
KOSTKA  = CUBE
# Polish:
SZESCIAN = CUBE
# German:
WUERFEL = CUBE
WURFEL = CUBE
# Spanish:
CUBO = CUBE
# Italian:
# Same as Spanish
# French:
# CUBE same as English

# ===================================================
# SQUARE
# ===================================================

def SQUARE(size):
    if size <= 0: 
        raise ExceptionWT("SQUARE(x) requires a positive value of x!")
    return BASEOBJ(CUBOID([size, size]))

# English:
# Czech::
CTVEREC = SQUARE
# Polish:
KWADRAT = SQUARE
# German:
QUADRAT = SQUARE
# Spanish:
CUADRADO = SQUARE
# Italian:
QUADRATO = SQUARE
# French:
CARRE = SQUARE

# ===================================================
# SQUARE3D
# ===================================================

def SQUARE3D (a):
    if a <= 0: 
        raise ExceptionWT("SQUARE3D(x) requires a positive value of x!")
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    return BASEOBJ(CUBOID([a, a, h]))

# English:
# Czech:
CTVEREC3D = SQUARE3D
# Polish:
KWADRAT3D = SQUARE3D
# German:
QUADRAT3D = SQUARE3D
# Spanish:
CUADRADO3D = SQUARE3D
# Italian:
QUADRATO3D = SQUARE3D
# French:
CARRE3D = SQUARE3D

# ===================================================
# BRICK, BOX
# ===================================================

def BOX(a, b, c = 0):   
    if c != 0: # the box is 3D
        if a <= 0 or b <= 0 or c < 0: raise ExceptionWT("BOX(x, y, z) requires positive dimensions x, y, z!")
        return BASEOBJ(CUBOID([a, b, c]))
    else:      # the box is 2D
        if a <= 0 or b <= 0: raise ExceptionWT("BOX(x, y) requires positive dimensions x, y!")
        return BASEOBJ(CUBOID([a, b]))
        
# English:
BRICK = BOX
# Czech::
KVADR = BRICK
CIHLA = BRICK
# Polish:
PUDLO = BRICK
CEGLA = BRICK
# German:
KASTEN = BRICK
SCHACHTEL = BRICK
# also BOX
# Spanish:
LADRILLO = BRICK
CAJA = BRICK
CUADRO = BRICK
# Italian:
COTTO = BRICK
SCATOLA = BRICK
MATTONE = BRICK
LATERIZIO = BRICK
PARALELLEPIPEDO = BRICK
# French:
BRIQUE = BRICK
BOITE = BRICK

# ===================================================
# RECTANGLE
# ===================================================

def RECTANGLE(a, b):
    if a <= 0 or b <= 0: raise ExceptionWT("RECTANGLE(x, y) requires positive dimensions x, y!")
    return BASEOBJ(CUBOID([a, b]))

# English:
RECT = RECTANGLE
# Czech:
OBDELNIK = RECTANGLE
# Polish:
PROSTOKAT = RECTANGLE
# German:
RECHTECK = RECTANGLE
# Spanish:
RECTANGULO = RECTANGLE
# Italian:
RETTANGOLO = RECTANGLE
# French:
# Same as in English

# ===================================================
# RECTANGLE3D
# ===================================================

def RECTANGLE3D(a, b):
    if a <= 0 or b <= 0: raise ExceptionWT("RECTANGLE3D(x, y) requires positive dimensions x, y!")
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    return BASEOBJ(CUBOID([a, b, h]))

# Czech::
OBDELNIK3D = RECTANGLE3D
# Polish:
PROSTOKAT3D = RECTANGLE3D
# German:
RECHTECK3D = RECTANGLE3D
# Spanish:
RECTANGULO3D = RECTANGLE3D
# Italian:
RETTANGOLO3D = RECTANGLE3D
# French:
# Same as in English

# ===================================================
# HEXAHEDRON
# ===================================================

def HEXAHEDRON(size):
    if size <= 0: raise ExceptionWT("HEXAHEDRON(x) requires a positive value of x!")
    c = CUBE(size)
    T(c, -0.5 * size, -0.5 * size, -0.5 * size)
    return c

# English:
HEX = HEXAHEDRON
# Czech:
HEXAEDR = HEXAHEDRON
# Polish:
# SZESCIAN already defined
# German:
HEXAEDER = HEXAHEDRON
# Spanish:
HEXAEDRO = HEXAHEDRON
# Italian:
ESAEDRO = HEXAHEDRON
# French:
HEXAEDRE = HEXAHEDRON

# ===================================================
# SIMPLEX
# ===================================================

def PLASM_SIMPLEX (dim):
    return Plasm.simplex(dim)

if self_test: 
	assert(Plasm.limits(PLASM_SIMPLEX(3))==Boxf(Vecf(1,0,0,0),Vecf(1,1,1,1)))

# NEW DEFINITION:
def SIMPLEX (dim):
    return BASEOBJ(Plasm.simplex(dim))


# ===================================================
# PRINT POL
# ===================================================

def PRINTPOL (obj):
    Plasm.Print(obj)
    return obj

def PRINT(obj):
    print obj
    return obj


# ===================================================
# POL DIMENSION
# ===================================================

def RN (pol): return Plasm.getSpaceDim(pol)
def PLASM_DIM (pol):return Plasm.getPointDim(pol)

def ISPOLDIM (dims):
    def ISPOLDIM1(pol):
        d = dims[0]
        n = dims[1]
        return  (d == PLASM_DIM(pol)) and (n == RN(pol))
    return ISPOLDIM1

if self_test: 
	assert(RN(Plasm.cube(2))==2 and PLASM_DIM(Plasm.cube(2))==2)

# ===================================================
# MKPOL
# ===================================================

def MKPOL (args_list):
   points, cells, pols = args_list
   dim = len(points[0])
   return Plasm.mkpol(dim, CAT(points), map(lambda x: [i-1 for i in x], cells),plasm_config.tolerance())

if self_test: 
	assert(Plasm.limits(MKPOL([  [[0,0],[1,0],[1,1],[0,1]] , [[1,2,3,4]] , None ]))==Boxf(Vecf(1,0,0),Vecf(1,1,1)))


# mkpol of a single point
MK = COMP([MKPOL, CONS([LIST, K([[1]]), K([[1]])])])

# ===================================================
# CONVEX HULL, CHULL
# ===================================================

# convex hull of points
def PLASM_CONVEXHULL (points):
    return MKPOL([points, [range(1,len(points)+1)], [[1]]])

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def CONVEXHULL(*args):
    list1 = list(args)
    if len(list1) == 1 and isinstance(list1[0], list) and isinstance(list1[0][0], list):    # User supplied a list of points
        list1 = list1[0]
    if len(list1) <= 2: raise ExceptionWT("CONVEXHULL(...) requires at least three points!")
    return BASEOBJ(PLASM_CONVEXHULL(list1))

# English:
CHULL = CONVEXHULL
CONVEX = CHULL
CH = CHULL
SPAN = CHULL
# Czech:
KONVEXNIOBAL = CHULL
KONVEX = CHULL
OBAL = CHULL
KOBAL = CHULL
# Polish:
OTOCZKAWYPUKLA = CHULL
OTOCZKA = CHULL
# German:
HUELLE = CHULL
HULLE = CHULL
SPANNE = CHULL
# Spanish:
CASCO = CHULL
CONVEXA = CHULL
# Italian:
CONVESSO = CHULL
SPANNA = CHULL
# French:
CONVEXE = CHULL
ENVELOPPE = CHULL
DUREE = CHULL

# ===================================================
# UKPOL
# ===================================================

def UKPOL (pol):  
    v= StdVectorFloat()
    u = StdVectorStdVectorInt()
    pointdim=Plasm.ukpol(pol, v, u) 
    points=[]
    for i in xrange(0, len(v), pointdim):points+=[[v[i] for i in range(i,i+pointdim)]]
    hulls=map(lambda x: [i + 1 for i in x], u)
    pols=[[1]]
    return  [points, hulls, pols]

if self_test: 
	assert(UKPOL(Plasm.cube(2))==[[[0,1],[0,0],[1,1],[1,0]],[[4,2,1,3]],[[1]]])

# return first point of a ukpol
UK = COMP([COMP([S1, S1]), UKPOL])



# ===================================================
# OPTIMIZE
# ===================================================

# not supported in new Python Plasm
def OPTIMIZE(pol): return pol

# ===================================================
# UKPOLF
# ===================================================

def UKPOLF (pol):  
	f = StdVectorFloat()
	u = StdVectorStdVectorInt()
	pointdim=Plasm.ukpolf(pol, f, u) 
	faces=[]
	for i in xrange(0, len(f), pointdim+1):
		faces+=[[f[i] for i in range(i,i+pointdim+1)]]
	hulls=map(lambda x: [i + 1 for i in x], u)
	pols=[[1]]
	return  [faces, hulls, pols]

if self_test:
	temp=UKPOLF(Plasm.cube(3))
	assert len(temp[0])==6 and len(temp[0][0])==4 and len(temp[1])==1 and len(temp[1][0])==6 and len(temp[2])==1


# ===================================================
# TRANSLATE
# ===================================================

def PLASM_TRANSLATE (axis):
    def PLASM_TRANSLATE1 (axis,values):
        def PLASM_TRANSLATE2 (axis,values,pol):
            axis    = [axis    ] if ISNUM(axis    ) else axis
            values= [values] if ISNUM(values) else values
            vt= Vecf(max(axis))
            for a,t in zip(axis,values):vt.set(a,t)
            return Plasm.translate(pol, vt)
        return lambda pol: PLASM_TRANSLATE2(axis,values,pol)    
    return lambda values: PLASM_TRANSLATE1(axis,values)
PLASM_T = PLASM_TRANSLATE

if self_test: 
	assert(Plasm.limits(PLASM_TRANSLATE([1, 2, 3])([0, 0, 2])(Plasm.cube(2)))==Boxf(Vecf(1,0,0,2),Vecf(1,1,1,2)))
	assert(Plasm.limits(PLASM_TRANSLATE([1, 2, 3])([1, 0, 2])(Plasm.cube(2)))==Boxf(Vecf(1,1,0,2),Vecf(1,2,1,2)))

# NEW DEFINITION:
# English:
# TRANSLATE EITHER ONE OBJECT OR LIST OF OBJECTS
def TRANSLATE(obj, t1, t2, t3 = 0):
    if not isinstance(obj, list):
        obj.move(t1, t2, t3)
    else:
        obj = flatten(obj)
        for oo in obj: 
            oo.move(t1, t2, t3)
    return COPY(obj)

T = TRANSLATE
MOVE = TRANSLATE
M = MOVE
SHIFT = TRANSLATE
# Czech:
POSUN = TRANSLATE
POSUNUTI = TRANSLATE
# Polish:
PRZENIES = TRANSLATE
PRZESUN = TRANSLATE
# German:
BEWEGE = TRANSLATE
BEWEGEN = TRANSLATE
BEWEGUNG = TRANSLATE
VERSCHIEBUNG = TRANSLATE
VERSCHIEBEN = TRANSLATE
VERSCHIEBE = TRANSLATE
# Spanish:
MOVER = TRANSLATE
MUEVA = TRANSLATE
MUEVE = TRANSLATE
# Italian:
MUOVERE = TRANSLATE
MUOVI = TRANSLATE
SPOSTARE = TRANSLATE
SPOSTA = TRANSLATE
# French:
DEPLACER = TRANSLATE
DEPLACE = TRANSLATE

# ===================================================
# SCALE
# ===================================================

def PLASM_SCALE (axis):
    def PLASM_SCALE1 (axis,values):
        def PLASM_SCALE2 (axis,values,pol):
            axis    = [axis    ] if ISNUM(axis    ) else axis
            values= [values] if ISNUM(values) else values
            dim=max(axis)
            vs = Vecf([1 for x in range(dim+1)]);vs.set(0,0.0)
            for a,t in zip(axis,values):vs.set(a,t)
            return Plasm.scale(pol, vs)
        return lambda pol: PLASM_SCALE2(axis,values,pol)    
    return lambda values: PLASM_SCALE1(axis,values)
PLASM_S = PLASM_SCALE

if self_test: 
	assert(Plasm.limits(PLASM_S(3)(2)(Plasm.cube(3)))==Boxf(Vecf(1,0,0,0),Vecf(1,1,1,2)))
	assert(Plasm.limits(PLASM_S([3,1])([4,2])(Plasm.cube(3)))==Boxf(Vecf(1,0,0,0),Vecf(1,2,1,4)))

# NEW DEFINITION:
# English:
# SCALE ONE OBJECT OR A LIST
def SCALE(obj, a, b, c = 1):
    if not isinstance(obj, list):
        obj.scale(a, b, c)
    else:
        obj = flatten(obj)
        for oo in obj: 
            oo.scale(a, b, c)
    return COPY(obj)

S = SCALE
# Czech:
SKALUJ = SCALE
SKALOVANI = SCALE
# Polish:
SKALUJ = SCALE
PRZESKALUJ = SCALE
# German:
SKALIERE = SCALE
SKALIEREN = SCALE
# Spanish:
ESCALA = SCALE
ESCALAR = SCALE
# Italian:
SCALA = SCALE
SCALARE = SCALE
# French:
ECHELLE = SCALE
REDIMENSIONNER = SCALE

# ===================================================
# ROTATE
# ===================================================

def PLASM_ROTATE (plane_indexes):
    def PLASM_ROTATE1 (angle):
        def PLASM_ROTATE2 (pol):
            dim = max(plane_indexes)
            return Plasm.rotate(pol, dim, plane_indexes[0] , plane_indexes[1], angle)
        return PLASM_ROTATE2    
    return PLASM_ROTATE1
PLASM_R = PLASM_ROTATE

if self_test: 
	assert(Plasm.limits(PLASM_ROTATE([1,2])(PI/2)(Plasm.cube(2))).fuzzyEqual(Boxf(Vecf(1,-1,0),Vecf(1,0,+1))))

# NEW DEFINITION
# English:
# ROTATE ONE OR MORE OBJECTS (ANGLE IN RADIANS)
def ROTATERAD(obj, angle_rad, axis = 3, point = [0, 0, 0]):
    if not isinstance(obj, list):
        obj.rotaterad(angle_rad, axis, point)
    else:
        obj = flatten(obj)
        for oo in obj: 
            oo.rotaterad(angle_rad, axis, point)
    return COPY(obj)
    
RRAD = ROTATERAD
# Czech:
OTOCRAD = ROTATERAD
OTOCENIRAD = ROTATERAD
ROTACERAD = ROTATERAD
ROTUJRAD = ROTATERAD
# Polish:
OBROCRAD = ROTATERAD
# German:
DREHERAD = ROTATERAD
DREHENRAD = ROTATERAD
DREHUNGRAD = ROTATERAD
ROTIERERAD = ROTATERAD
ROTIERENRAD = ROTATERAD
ROTIERUNGRAD = ROTATERAD
# Spanish:
GIRARAD = ROTATERAD
ROTARAD = ROTATERAD
GIRARRAD = ROTATERAD
ROTARRAD = ROTATERAD
# Italian:
RUOTARERAD = ROTATERAD
RUOTARAD = ROTATERAD
# French:
TOURNERRAD = ROTATERAD
TOURNERAD = ROTATERAD

# English:
# ROTATE ONE OR MORE OBJECTS (ANGLE IN DEGREES)
def ROTATEDEG(obj, angle_deg, axis = 3, point = [0, 0, 0]):
    if not isinstance(obj, list):
        obj.rotate(angle_deg, axis, point)
    else:
        obj = flatten(obj)
        for oo in obj: 
            oo.rotate(angle_deg, axis, point)
    return COPY(obj)

ROTATE = ROTATEDEG
RDEG = ROTATEDEG
R = ROTATEDEG
# Czech:
OTOC = ROTATEDEG
OTOCENI = ROTATEDEG
ROTACE = ROTATEDEG
ROTUJ = ROTATEDEG
# Polish:
OBROC = ROTATEDEG
# German:
DREHE = ROTATEDEG
DREHEN = ROTATEDEG
DREHUNG = ROTATEDEG
ROTIERE = ROTATEDEG
ROTIEREN = ROTATEDEG
ROTIERUNG = ROTATEDEG
# Spanish:
GIRA = ROTATE
ROTA = ROTATE
GIRAR = ROTATE
ROTAR = ROTATE
# Italian:
RUOTARE = ROTATE
RUOTA = ROTATE
# French:
TOURNER = ROTATE
TOURNE = ROTATE

# ===================================================================
# RELATIVE ROTATION - ABOUT THE OBJECT'S OWN CENTER - ONE OBJECT ONLY
# ===================================================================

# English:
def RR(obj, angle_deg, axis = 3):
    if isinstance(obj, list):
        raise ExceptionWT("Command ROTATEREL (rotation about objects own center) can only be applied to a single object!")
    obj.rotaterel(angle_deg, axis)
    return COPY(obj)
ROTATER = RR
RREL = RR
ROTATEREL = RR

# ===================================================
#; Applica uno shearing con vettore shearing-vector-list sulla variabile
#; i-esima del complesso poliedrale pol-complex
# ===================================================

def SHEARING (i):
    def SHEARING1 (shearing_vector_list):
        def SHEARING2 (pol):
            raise Exception("Shearing not implemented!")
        return SHEARING2    
    return SHEARING1
H = SHEARING
       
# ===================================================
# generic matrix
# ===================================================
def MAT (matrix):
    def MAT0 (pol):
        vmat= Matf(CAT(matrix))
        return Plasm.transform(pol,vmat,vmat.invert() )
    return MAT0   

if self_test: 
	assert(Plasm.limits(MAT([[1,0,0],[1,1,0],[2,0,1]])(Plasm.cube(2)))==Boxf(Vecf(1,1,2),Vecf(1,2,3)))

# ===================================================
# EMBED
# ===================================================

def EMBED (up_dim):
    def EMBED1 (pol):
        new_dim_pol = Plasm.getSpaceDim(pol) + up_dim
        return Plasm.embed(pol,new_dim_pol)
    return EMBED1    

# NEW DEFINITION:
def FOOTPRINT(obj):
    return EMBED(1)(PLASM_BOX([1,2])(obj))

# ===================================================
# STRUCT
# ===================================================

def PLASM_STRUCT(seq,nrec=0):

	if not isinstance(seq,list) : 
		raise Exception("PLASM_STRUCT must be applied to a list!")
	
	if (len(seq)==0):
		raise Exception("PLASM_STRUCT must be applied to a non-empty list!")
	
	# avoid side effect
	if (nrec==0): seq=[x for x in seq] 
	
	# accumulate pols without transformations
	pols=[]
	while len(seq)>0 and ISPOL(seq[0]):
		pols+=[seq[0]]; seq=seq[1:]
	
	# accumulate transformations for pols
	transformations=[]
	while len(seq)>0 and ISFUN(seq[0]): 
		transformations+=[seq[0]]; seq=seq[1:]
	
	# avoid deadlock, i.e. call the recursion on invalid arguments
	if len(seq)>0 and not ISPOL(seq[0]) and not ISFUN(seq[0]):
		raise Exception("PLASM_STRUCT arguments not valid, not all elements are polygons or transformations!")
	
	if len(seq)>0:
		assert ISPOL(seq[0]) # eaten all trasformations, the next must be a pol!
		child=PLASM_STRUCT(seq,nrec+1)
		assert ISPOL(child)
		if (len(transformations)>0): child=COMP(transformations)(child)
		pols+=[child]
	
	if len(pols)==0:
		raise Exception("Cannot find geometry in PLASM_STRUCT, found only transformations!")
	
	return Plasm.Struct(pols)     

if self_test: 
	assert(Plasm.limits(PLASM_STRUCT([Plasm.cube(2)  ,  PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]) ,  PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]) ,  Plasm.cube(2),Plasm.cube(2,1,2)  ])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,4,4))))
	assert(Plasm.limits(PLASM_STRUCT([ PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]), PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]), Plasm.cube(2)  ,  PLASM_TRANSLATE([1, 2, 3])([1, 1, 0])  ,PLASM_TRANSLATE([1, 2, 3])([1, 1, 0]),  Plasm.cube(2),Plasm.cube(2,1,2)  ])).fuzzyEqual(Boxf(Vecf(1,2,2),Vecf(1,6,6))))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
# English:
# NEW DEFINITION - STRUCT IS JUST A LIST, IT CAN BE EASILY DECOMPOSED
# BACK INTO INDIVIDUAL OBJECTS WHICH IS VERY MUCH NEEDED
def STRUCT(*args):
    list1 = list(args)
    list1 = flatten(list1) # flatten the rest as there may be structs
    if len(list1) < 1: raise ExceptionWT("STRUCT() must be applied to some objects!")
    return list1
# OLD DEFINITION - THERE WERE PROBLEMS WITH COLORS
#def STRUCT(*args):
#    list1 = list(args)
#    if len(list1) <= 1: raise ExceptionWT("STRUCT(...) requires at least two objects!")
#    return PLASM_STRUCT(list1)
# Czech:
SPOJ = STRUCT
SPOJIT = STRUCT
SPOJENI = STRUCT
STRUKTURA = STRUCT
# Polish:
# It is also "STRUKTURA"
#German:
STRUKTUR = STRUCT
VERBINDE = STRUCT
# Spanish:
ESTRUCTURA = STRUCT
ESTRUCT = STRUCT
# Italian:
STRUTTURA = STRUCT
# French:
# Same as English

# ===================================================
# BOOLEAN OP
# ===================================================

#also +, or SUM, can be used to indicate UNION
# THIS WAS TOO COMPUTATIONALLY EXPENSIVE, NOT USED ANYMORE
def PLASM_UNION(objs_list):
        color = PLASM_GETCOLOR(objs_list[0])
        result = Plasm.boolop(BOOL_CODE_OR, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())
        if color != []: return COLOR(result, color)
	else: return result

# ===================================================
# WELD = HARD UNION (ORIGINAL, COMPUTATIONALLY EXPENSIVE)
# ===================================================

def WELD(*args):
    objs = list(args)
    objs = flatten(objs)
    geoms = []
    for x in objs:
        geoms.append(x.geom)
    color = objs[0].getcolor()
    result = BASEOBJ(Plasm.boolop(BOOL_CODE_OR, geoms, plasm_config.tolerance(), plasm_config.maxnumtry(), plasm_config.useOctreePlanes()))
    result.setcolor(color)
    return result


# ===================================================
# SOFT UNION = STRUCT
# ===================================================

# NEW DEFINITION - UNION IS JUST STRUCT
def UNION(*args):
    list1 = list(args)
    list1 = flatten(list1) # flatten the rest as there may be structs
    if len(list1) < 2: raise ExceptionWT("UNION() must be applied to at least two objects!")
    return list1

# English:
U = UNION
SUM = UNION
# Czech:
SJEDNOCENI = UNION
SOUCET = UNION
SECTI = UNION
SECIST = UNION
SUMA = UNION
# Polish:
UNIA = UNION
SUMA = UNION
# German:
VEREINIGE = UNION
VEREINIGUNG = UNION
SUMME = UNION
# Spanish:
SUMA = UNION
# Italian:
SOMMA = UNION
UNIONE = UNION
# French:
# UNION same as English
SOMME = UNION

#also ^ can be used to indicates INTERSECTION
def PLASM_INTERSECTION (objs_list):
    result = Plasm.boolop(BOOL_CODE_AND, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())
    return result

PLASM_I = PLASM_INTERSECTION

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
# English:
def INTERSECTION(*args):
    list1 = list(args)
    l = len(list1)
    if l < 2: 
        raise ExceptionWT("INTERSECTION(...) requires at least two objects!")
    for i in range(1, l):
        if isinstance(list1[i], list):
            raise ExceptionWT("Only the first argument of INTERSECTION(...) may be a struct (list)!")

    item1 = list1[0] # this is either a single item or a list
    if not isinstance(item1, list):
        geoms = []
        for x in list1:
            geoms.append(x.geom)
        obj = BASEOBJ(PLASM_INTERSECTION(geoms))
        obj.setcolor(list1[0].color)
        return obj
    else:
        item1 = list1.pop(0)
        item1flat = flatten(item1)
        result = []
        for x in item1flat:
            list1_new = [x] + list1
            geoms = []
            for y in list1_new:
                geoms.append(y.geom)
            obj = BASEOBJ(PLASM_INTERSECTION(geoms))
            obj.setcolor(list1_new[0].color)
            result.append(obj)
        return result

I = INTERSECTION
# Czech:
PRUNIK = INTERSECTION
# Polish:
PRZECIECIE = INTERSECTION
PRZETNIJ = INTERSECTION
# German:
DURCHSCHNITT = INTERSECTION
SCHNITT = INTERSECTION
SCHNEIDE = INTERSECTION
# Spanish:
INTERSECCION = INTERSECTION
# Italian:
INTERSEZIONE = INTERSECTION
INTERSECA = INTERSECTION
# French:
# Same as English

#also -, or DIFF, can be used to indicates DIFFERENCE
def PLASM_DIFFERENCE (objs_list):
        result = Plasm.boolop(BOOL_CODE_DIFF, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())
	return result

PLASM_DIFF = PLASM_DIFFERENCE        

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
# AND FIRST ITEM CAN BE A LIST (THAT PLAYS THE ROLE OF A STRUCT)
# English:
def DIFFERENCE(*args):
    list1 = list(args)
    if len(list1) < 2: 
        raise ExceptionWT("DIFFERENCE(...) requires at least two objects!")
    item1 = list1[0] # this is either a single item or a list
    item2 = list1[1] # this is either a single item or a list
    if isinstance(item1, list) and isinstance(item2, list):
        raise ExceptionWT("DIFFERENCE(...): Subtracting of a struct (list) from another struct is not allowed.")
    if not isinstance(item1, list):
        item1 = list1.pop(0)
        list1 = flatten(list1) # flatten the rest as there may be structs
        list1 = [item1] + list1
	geoms = []
        for x in list1:
            geoms.append(x.geom)
        obj = BASEOBJ(PLASM_DIFF(geoms))
        obj.setcolor(item1.color)
        return obj
    else:
        list2 = list1.pop(0)
        list1 = flatten(list1) # flatten the rest as there may be structs
        result = []
        for x in list2:
            list1_new = [x] + list1
   	    geoms = []
            for y in list1_new:
                geoms.append(y.geom)
	    obj = BASEOBJ(PLASM_DIFF(geoms))
	    obj.setcolor(x.color)
            result.append(obj)
        return result

# OLD DEFINITION
#def DIFFERENCE(*args):
#    list1 = list(args)
#    if len(list1) <= 1: raise ExceptionWT("DIFFERENCE(...) requires at least two objects!")
#    return PLASM_DIFFERENCE(list1)
DIFF = DIFFERENCE
D = DIFF
SUBTRACT = DIFF
# Czech:
ROZDIL = DIFF
ODECTI = DIFF
ODECIST = DIFF
MINUS = DIFF
# Polish:
ROZNICA = DIFF
ODEJMIJ = DIFF
# German:
DIFFERENZ = DIFF
ABZIEHE = DIFF
SUBTRAHIERE = DIFF
# Spanish:
DIFERENCIA = DIFF
SUSTRAER = DIFF
SUSTRAE = DIFF
DIF = DIFF
# Italian:
DIFERENCIA = DIFF
SOTTRARRE = DIFF
SOTTRAI = DIFF
# French:
SOUSTRAIRE = DIFF
SOUSTRAIS = DIFF
# DIFF same as in English

# ===================================================
# XOR
# ===================================================

# original definition, now internal
def PLASM_XOR(objs_list):
    result = Plasm.boolop(BOOL_CODE_XOR, objs_list,plasm_config.tolerance(),plasm_config.maxnumtry(),plasm_config.useOctreePlanes())
    return result

# NEW DEFINITION, JUST FOR TWO OBJECTS
def XOR(a, b):
    L = []
    L.append(DIFF(a, b))    
    L.append(DIFF(b, a))    
    return L

if self_test: 
	assert(Plasm.limits(PLASM_UNION([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1.5,1.5))))
	assert(Plasm.limits(PLASM_INTERSECTION([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0.5,0.5),Vecf(1,1,1))))
	assert(Plasm.limits(PLASM_DIFFERENCE([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1,1))))
	assert(Plasm.limits(PLASM_XOR([Plasm.cube(2,0,1),Plasm.cube(2,0.5,1.5)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1.5,1.5))))

# ===================================================
# JOIN
# ===================================================

def PLASM_JOIN (pol_list):
   if  ISPOL(pol_list): pol_list=[pol_list]
   return Plasm.join(pol_list,plasm_config.tolerance())
   
if self_test: 
	assert(Plasm.limits(PLASM_JOIN([Plasm.cube(2,0,1)])).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1,1))))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS FOR TWO OBJECTS)
def JOIN(a, b = None):
    if b != None:
        return PLASM_JOIN([a, b])
    else: # single argument must be list
        return PLASM_JOIN(a)


# ===================================================
# also ** can be used to indicates POWER
# ===================================================

def PLASM_POWER (objs_list):
     
     if not isinstance(objs_list,list) or len(objs_list)!=2:
        raise ExceptionWT("POWER(b, h) requires two arguments: 2D object b and a height h!") 

     if ISNUM(objs_list[0]) and ISNUM(objs_list[1]):
        return math.pow(objs_list[0], objs_list[1])

     return Plasm.power(objs_list[0], objs_list[1])
        
if self_test: 
	assert(PLASM_POWER([2,2])==4)
	assert(Plasm.limits(PLASM_POWER([Plasm.cube(2),Plasm.cube(1)])).fuzzyEqual(Boxf(Vecf(1,0,0,0),Vecf(1,1,1,1))))

# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
def PRODUCT(*args):
    list1 = list(args)
    if len(list1) != 2: 
        raise Exception("POWER(...) requires two arguments!")
    list2 = []
    color = list1[0].color
    for x in list1:
        list2.append(x.geom)
    obj = BASEOBJ(PLASM_POWER(list2))
    obj.setcolor(color)
    return obj

# English:
POWER = PRODUCT
# Czech:
MOCNINA = POWER
PRODUKT = POWER
SOUCIN = POWER
UMOCNIT = POWER
UMOCNI = POWER
# Polish:
MOC = POWER
ILOCZYN = POWER
#PRODUKT = POWER
# German:
LEISTUNG = POWER
PRODUKT = POWER
# Spanish:
POTENCIA = POWER
PRODUCTO = POWER
# Italian:
POTENZA = POWER
#PRODUCTO = POWER
# French:
PUISSANCE = POWER
PRODUIT = POWER


# ===================================================
# Skeleton
# ===================================================
def SKELETON (ord):
    def SKELETON_ORDER (pol):
        return Plasm.skeleton(pol, ord)
    return SKELETON_ORDER

SKEL_0 =  SKELETON(0)
SKEL_1 =  SKELETON(1)
SKEL_2 =  SKELETON(2)
SKEL_3 =  SKELETON(3)
SKEL_4 =  SKELETON(4)
SKEL_5 =  SKELETON(5)
SKEL_6 =  SKELETON(6)
SKEL_7 =  SKELETON(7)
SKEL_8 =  SKELETON(8)
SKEL_9 =  SKELETON(9)

if self_test: 
	assert( Plasm.limits(SKELETON(0)(Plasm.cube(2))).fuzzyEqual(Boxf(Vecf(1,0,0),Vecf(1,1,1))) )


# ===================================================
# FLATTEN
# ===================================================

# takes lists (possibly including other lists) and returns one plain list
def flatten(*args):
    output = []
    for arg in args:
        if hasattr(arg, '__iter__'):
            output.extend(flatten(*arg))
        else:
            output.append(arg)
    return output

FLATTEN = flatten

# ===================================================
# GRID
# ===================================================

# original definition:
def PLASM_GRID (*args):
    sequence = flatten(*args)
    if len(sequence) == 0: raise ExceptionWT("GRID(...) requires at least one interval length!")
    cursor,points,hulls= (0,[[0]],[])
    for value in sequence:
        points = points + [[cursor + abs(value)]] 
        if value>=0: hulls += [[len(points)-2,len(points)-1]]
        cursor = cursor + abs(value)
    return  Plasm.mkpol(1, CAT(points), hulls,plasm_config.tolerance())   
PLASM_QUOTE = PLASM_GRID

# NEW DEFINITION:
def GRID(*args):
    sequence = flatten(*args)
    if len(sequence) == 0: 
        raise ExceptionWT("GRID(...) requires at least one interval length!")
    cursor,points,hulls= (0,[[0]],[])
    for value in sequence:
        points = points + [[cursor + abs(value)]] 
        if value>=0: hulls += [[len(points)-2,len(points)-1]]
        cursor = cursor + abs(value)
    obj = BASEOBJ(Plasm.mkpol(1, CAT(points), hulls,plasm_config.tolerance()))
    return obj

# English:
QUOTE = GRID
# Czech:
SIT = GRID
MRIZ = GRID
# Polish:
SIATKA = GRID
# German:
GITTER = GRID
NETZ = GRID
# Spanish:
REJILLA = GRID
CUADRICULA = GRID
# Italian:
GRIGLIA = GRID
# French:
GRILLE = GRID

if self_test: 
	assert(Plasm.limits(PLASM_QUOTE([1,-1,1]))==Boxf(Vecf([1,0]),Vecf([1,3])))
	assert(Plasm.limits(PLASM_QUOTE([-1,1,-1,1]))==Boxf(Vecf([1,1]),Vecf([1,4])))


Q = COMP([PLASM_QUOTE, IF([ISSEQ, ID, CONS([ID])])])

# ===================================================
# INTERVALS 
# ===================================================

def PLASM_INTERVALS (A):
    def PLASM_INTERVALS0 (N):
        return PLASM_QUOTE([float(A)/float(N) for i in range(N)])
    return PLASM_INTERVALS0

if self_test:
    assert Plasm.limits(PLASM_INTERVALS(10)(8))==Boxf(Vecf([1,0]),Vecf([1,10]))

# NEW DEFINITION:
def INTERVALS(a, n):
    return PLASM_INTERVALS(a)(n)
DIVISION = INTERVALS
# Czech:
DELENI = INTERVALS
INTERVALY = INTERVALS
# Polish:
DZIELENIE = INTERVALS
INTERWALY = INTERVALS
# German:
INTERVALLE = INTERVALS
AUFTEILEN = INTERVALS
AUFSPALTEN = INTERVALS
# Spanish:
# DIVISION same as in English
# Italian:
# DIVISION same as in English
DIVISIONE = INTERVALS
# French:
# DIVISION same as in English

# ===================================================
# SIZE
# ===================================================

def PLASM_SIZE (List):
    def PLASM_SIZE1 (pol): 
        size = Plasm.limits(pol).size()
        return [size[i] for i in List] if isinstance(List,list) else size[List]
    return PLASM_SIZE1

if self_test: 
	assert(PLASM_SIZE(1)(Plasm.cube(2))==1)
	assert(PLASM_SIZE([1,3])(PLASM_SCALE([1, 2, 3])([1, 2, 3])(Plasm.cube(3)))==[1,3])

# NEW_DEFINITION:
def SIZE(pol, List):
    return PLASM_SIZE(List)(pol.geom)
# Czech:
VELIKOST = SIZE
ROZMER = SIZE
DELKA = SIZE
# Polish:
ROZMIAR = SIZE
# German:
GROESSE = SIZE
GROSSE = SIZE
LAENGE = SIZE
LANGE = SIZE
# Spanish:
TAMANO = SIZE
LONGITUD = SIZE
# Italian:
TAGLIA = SIZE
LUNGHEZZA = SIZE
# French:
TAILLE = SIZE
LONGUEUR = SIZE



# ===================================================
# MIN/MAX/MID
# ===================================================
def MIN  (List):
    def MIN1 (pol):
        box = Plasm.limits(pol)
        return [box.p1[i] for i in List] if isinstance(List,list) else box.p1[List]
    return MIN1
    
def MAX  (List):
    def MAX1 (pol):
        box = Plasm.limits(pol)
        return [box.p2[i] for i in List] if isinstance(List,list) else box.p2[List]
    return MAX1


def MID  (List):
    def MID1 (pol):
        center = Plasm.limits(pol).center()
        return [center [i] for i in List] if isinstance(List,list) else center[List]
    return MID1

def MINX(obj):
    return obj.minx()
def MINY(obj):
    return obj.miny() 
def MINZ(obj):
    return obj.minz() 
def MAXX(obj):
    return obj.maxx() 
def MAXY(obj):
    return obj.maxy() 
def MAXZ(obj):
    return obj.maxz() 

if self_test: 
	assert(MIN(1)(Plasm.cube(2))==0)
	assert(MIN([1,3])(PLASM_TRANSLATE([1, 2, 3])([10, 20, 30])(Plasm.cube(3)))==[10,30])
	assert(MAX(1)(Plasm.cube(2))==1)
	assert(MAX([1,3])(PLASM_TRANSLATE([1, 2, 3])([10, 20, 30])(Plasm.cube(3)))==[11,31])
	assert(MID(1)(Plasm.cube(2))==0.5)
	assert(MID([1,3])(Plasm.cube(3))==[0.5,0.5])



# ======================================
# identity matrix
# ======================================
def IDNT (N):
    return [ [ 1 if r==c else 0 for c in range(0,N) ] for r in range(0,N)]

if self_test: 
	assert(IDNT(0)==[] and IDNT(2)==[[1,0],[0,1]])

# =============================================
# split 2PI in N parts
# =============================================

def SPLIT_2PI(N):
   delta=2*PI/N
   return [i*delta for i in range(0,N)]

if self_test: 
	assert(SPLIT_2PI(4)[2]==PI)

# NEW DEFINITIONS:
# MOVE THE SECOND OBJECT TO BE CENTERED ON TOP THE FIRST ONE
def TOP(obj1, obj2): # obj2 goes on top of obj1
    if isinstance(obj2, list):
        raise ExceptionWT("Second argument of TOP(...) may not be a list!")
    if not isinstance(obj1, list):
        # z-direction:
        maxz1 = obj1.maxz()
        minz2 = obj2.minz()
        T(obj2, 0, 0, maxz1 - minz2)    
        # x-direction:
        cx1 = 0.5*(obj1.minx() + obj1.maxx())
        cx2 = 0.5*(obj2.minx() + obj2.maxx())
        T(obj2, cx1 - cx2, 0, 0)
        # y-direction:
        cy1 = 0.5*(obj1.miny() + obj1.maxy())
        cy2 = 0.5*(obj2.miny() + obj2.maxy())
        T(obj2, 0, cy1 - cy2, 0)
        return U(obj1, obj2)
    else:
        maxx1 = obj1[0].maxx()
        minx1 = obj1[0].minx()
        maxy1 = obj1[0].maxy()
        miny1 = obj1[0].miny()
        maxz1 = obj1[0].maxz()
        minz1 = obj1[0].minz()
        for x in obj1:
            if x.maxx() > maxx1: maxx1 = x.maxx()
            if x.minx() < minx1: minx1 = x.minx()
            if x.maxy() > maxy1: maxy1 = x.maxy()
            if x.miny() < miny1: miny1 = x.miny()
            if x.maxz() > maxz1: maxz1 = x.maxz()
            if x.minz() < minz1: minz1 = x.minz()
        # z-direction:
        minz2 = obj2.minz()
        T(obj2, 0, 0, maxz1 - minz2)    
        # x-direction:
        cx1 = 0.5*(minx1 + maxx1)
        cx2 = 0.5*(obj2.minx() + obj2.maxx())
        T(obj2, cx1 - cx2, 0, 0)
        # y-direction:
        cy1 = 0.5*(miny1 + maxy1)
        cy2 = 0.5*(obj2.miny() + obj2.maxy())
        T(obj2, 0, cy1 - cy2, 0)
        return U(obj1, obj2)
        

# MOVE THE SECOND OBJECT TO BE CENTERED BELOW THE FIRST ONE
def BOTTOM(obj1, obj2):
    R(obj1, 180, 1)    
    R(obj2, 180, 1)
    TOP(obj1, obj2)
    R(obj1, -180, 1)    
    R(obj2, -180, 1)
    return U(obj1, obj2)

# MOVE THE SECOND OBJECT TO BE CENTERED ON THE LEFT OF THE FIRST ONE
def LEFT(obj1, obj2):
    R(obj1, -90, 2)    
    R(obj2, -90, 2)
    TOP(obj1, obj2)
    R(obj1, 90, 2)    
    R(obj2, 90, 2)
    return U(obj1, obj2)
  
# MOVE THE SECOND OBJECT TO BE CENTERED ON THE RIGHT OF THE FIRST ONE
def RIGHT(obj1, obj2):
    R(obj1, 90, 2)    
    R(obj2, 90, 2)
    TOP(obj1, obj2)
    R(obj1, -90, 2)    
    R(obj2, -90, 2)
    return U(obj1, obj2)
   
# MOVE THE SECOND OBJECT TO BE CENTERED ON THE FRONT OF THE FIRST ONE
def FRONT(obj1, obj2):
    R(obj1, -90, 1)    
    R(obj2, -90, 1)
    TOP(obj1, obj2)
    R(obj1, 90, 1)    
    R(obj2, 90, 1)
    return U(obj1, obj2)

# MOVE THE SECOND OBJECT TO BE CENTERED ON THE REAR OF THE FIRST ONE
def REAR(obj1, obj2):
    R(obj1, 90, 1)    
    R(obj2, 90, 1)
    TOP(obj1, obj2)
    R(obj1, -90, 1)    
    R(obj2, -90, 1)
    return U(obj1, obj2)

# ===================================================
# PLASM_BOX of a pol complex
# ===================================================

def PLASM_BOX (List):
    def PLASM_BOX0 (List,pol):
        if not isinstance(List,list): List=[List]
        dim = len(List) 
        box=Plasm.limits(pol)
        vt =Vecf([0] + [box.p1     [i] for i in List])
        vs=Vecf([0] + [box.size()[i] for i in List]) 
        return Plasm.translate(Plasm.scale(Plasm.cube(dim),vs),vt)
    return lambda pol: PLASM_BOX0(List,pol)

if self_test: 
   assert(Plasm.limits(PLASM_BOX([1,3])(Plasm.translate(Plasm.cube(3),Vecf(0,1,2,3))))==Boxf(Vecf(1,1,3),Vecf(1,2,4))) 
   assert(Plasm.limits(PLASM_BOX(3)(Plasm.translate(Plasm.cube(3),Vecf(0,1,2,3))))==Boxf(Vecf([1,3]),Vecf([1,4])))

# ===================================================
# VECTORS 
# ===================================================

def VECTPROD (args):
    ret=Vec3f(args[0]).cross(Vec3f(args[1]))
    return [ret.x,ret.y,ret.z]

if self_test:
   assert VECTPROD ([[1,0,0],[0,1,0]])==[0,0,1]
   assert VECTPROD ([[0,1,0],[0,0,1]])==[1,0,0] 
   assert VECTPROD ([[0,0,1],[1,0,0]])==[0,1,0]


def VECTNORM(u):
   return Vecf(u).module()

if self_test: 
	assert VECTNORM([1,0,0])==1 


INNERPROD = COMP([COMP([RAISE(PLASM_SUM), AA(RAISE(PLASM_PROD))]), TRANS])

if self_test:
  assert INNERPROD ([[1,2,3],[4,5,6]])==32


def SCALARVECTPROD (args):
    s,l=args
    if not isinstance(l,list): s,l=l,s
    return [s*l[i] for i in range(len(l))]

if self_test:
  assert SCALARVECTPROD([2,[0,1,2]])==[0,2,4] and SCALARVECTPROD([[0,1,2],2])==[0,2,4]


def MIXEDPROD (args):
    A , B , C = args
    return INNERPROD([VECTPROD([A,B]),C])


if self_test:
	assert MIXEDPROD([[1,0,0],[0,1,0],[0,0,1]])==1.0
	
def UNITVECT(V):
	assert isinstance(V,list)
	v=Vecf(V).normalize()
	return [v[i] for i in range(len(V))]
	
if self_test:
	assert UNITVECT([2,0,0])==[1,0,0]
	assert UNITVECT([1,1,1])==UNITVECT([2,2,2])


def DIRPROJECT (E):
	E=UNITVECT(E)
	def DIRPROJECT0 (V):
		return SCALARVECTPROD([(INNERPROD([E,V])),E])
	return DIRPROJECT0

if self_test:
	assert DIRPROJECT([1,0,0])([2,0,0])==[2,0,0]
	assert DIRPROJECT([1,0,0])([0,1,0])==[0,0,0]

def ORTHOPROJECT (E):
    def ORTHOPROJECT0 (V):
        return VECTDIFF([V,DIRPROJECT((E))(V)])
    return ORTHOPROJECT0

if self_test:
	assert ORTHOPROJECT([1,0,0])([1,1,0])==[0,1,0]




# ===================================================
# PLASM_MAP
# ===================================================

def PLASM_MAP(fun):

	# speed up by caching points
	cache={}

	def PLASM_MAP0 (fun,pol):

		points, hulls, pols = UKPOL(pol)

		if isinstance(fun, list): 
			fun = CONS(fun)    

		# do not calculate the same points two times
		mapped_points=[]

		for point in points:

			key=str(point)

			if key in cache:
				# already calculated
				mapped_point=cache[key]
			else:
				# to calculate (slow!)
				mapped_point=fun(point)
				cache[key]=mapped_point

			mapped_points+=[mapped_point]

		return MKPOL([mapped_points, hulls, pols])

	return lambda pol: PLASM_MAP0(fun,pol)


if self_test: 
	assert( Plasm.limits(PLASM_MAP([S1,S2])(Plasm.cube(2)))==Boxf(Vecf(1,0,0),Vecf(1,1,1)))
	assert(Plasm.limits(PLASM_MAP(ID)(Plasm.cube(2)))==Boxf(Vecf(1,0,0),Vecf(1,1,1)))

# NEW DEFINITION:
def MAP(ref_domain, args):
    return PLASM_MAP(args)(ref_domain)

# ===================================================
# OTHER TESTS
# ===================================================

ISREALVECT = ISSEQOF(ISREAL)
ISFUNVECT = ISSEQOF(ISFUN)
ISVECT = COMP([OR, CONS([ISREALVECT, ISFUNVECT])])
ISPOINT = ISVECT
ISPOINTSEQ = COMP([AND, CONS([ISSEQOF(ISPOINT), COMP([EQ, AA(LEN)])])])
ISMAT = COMP([AND, CONS([COMP([OR, CONS([ISSEQOF(ISREALVECT), ISSEQOF(ISFUNVECT)])]), COMP([EQ, AA(LEN)])])])
ISSQRMAT = COMP([AND, CONS([ISMAT, COMP([EQ, CONS([LEN, COMP([LEN, S1])])])])])
def ISMATOF (ISTYPE): return COMP([COMP([AND, AR]), CONS([COMP([AA(ISTYPE), CAT]), COMP([ISMAT, (COMP([AA, AA]))((K(1)))])])])



# ===================================================
# FACT  
# ===================================================

def FACT (N):
    return PLASM_PROD(INTSTO(N)) if N>0 else 1

if self_test: 
	assert FACT(4)==24 and FACT(0)==1


# =============================================
# circle 
# =============================================

def CIRCLE_POINTS(R, N):
   return [ [R*math.cos(i*2*PI/N),R*math.sin(i*2*PI/N)] for i in range(0,N) ]

def CIRCUMFERENCE (R):
    return lambda N: PLASM_MAP(lambda p: [R*math.cos(p[0]),R*math.sin(p[0]) ])(PLASM_INTERVALS(2*PI)(N))

def NGON (N):
    return CIRCUMFERENCE(1)(N)


if self_test:
    assert Plasm.limits(CIRCUMFERENCE(1)(8))==Boxf(Vecf(1,-1,-1),Vecf(1,+1,+1))
    assert len(  (UKPOL(CIRCUMFERENCE(1)(4)))[0]  )==4*2 

# =============================================
# RING 
# =============================================

def PLASM_RING (radius):
    R1 , R2 = radius
    def PLASM_RING0 (subds):
        N , M = subds
        domain= Plasm.translate(PLASM_POWER([PLASM_INTERVALS(2*PI)(N),PLASM_INTERVALS(R2-R1)(M)]),Vecf([0.0,0.0,R1]))
        fun=lambda p: [p[1]*math.cos(p[0]),p[1]*math.sin(p[0])]
        return PLASM_MAP(fun)(domain)
    return PLASM_RING0

if self_test:
    assert Plasm.limits(PLASM_RING([0.5,1])([8,8]))==Boxf(Vecf(1,-1,-1),Vecf(1,+1,+1))

# NEW DEFINITION
def RING(r1, r2, division = [64, 1]):
    if r1 <= 0: 
        raise ExceptionWT("Inner radius r1 in RING(r1, r2) must be positive!")
    if r2 <= 0: 
        raise ExceptionWT("Outer radius r2 in RING(r1, r2) must be positive!")
    if r1 >= r2: 
        raise ExceptionWT("Inner radius r1 must be smaller than outer radius r2 in RING(r1, r2)!")
    obj = BASEOBJ(CUBOID([1, 1, 1])) # just to create the variable
    if type(division) == list: 
        obj = BASEOBJ(PLASM_RING([r1, r2])(division))
    else:
        if division < 3: 
            raise ExceptionWT("Number of edges n in RING(r1, r2, n) must be at least 3!")
        else: obj = BASEOBJ(PLASM_RING([r1, r2])([division, 1]))
    return obj

# Czech
# TODO

# =============================================
# TUBE
# =============================================

def PLASM_TUBE (args):
    r1 , r2 , height= args
    def PLASM_TUBE0 (N):
        return Plasm.power(PLASM_RING([r1, r2])([N, 1]), PLASM_QUOTE([height]))
    return PLASM_TUBE0

# NEW DEFINITION
# English:
def TUBE(r1, r2, h, division = 64):
    if r1 <= 0: 
        raise ExceptionWT("Inner radius r1 in TUBE(r1, r2, h) must be positive!")
    if r2 <= 0: 
        raise ExceptionWT("Outer radius r2 in TUBE(r1, r2, h) must be positive!")
    if h <= 0: 
        raise ExceptionWT("Height h in TUBE(r1, r2, h) must be positive!")
    if r1 >= r2: 
        raise ExceptionWT("Inner radius r1 must be smaller than outer radius r2 in TUBE(r1, r2, h)!")
    if division < 3: 
        raise ExceptionWT("The number of sides n in TUBE(r1, r2, h, n) must be at least 3!")
    return BASEOBJ(PLASM_TUBE([r1, r2, h])(division))
# Czech:
TRUBICE = TUBE
TRUBKA = TUBE
TUBA = TUBE
ROURA = TUBE
# Polish:
RURA = TUBE
# German:
ROHR = TUBE
# Spanish:
TUBO = TUBE
# Italian:
# Same as in Spanish
# French:
# Same as in English

# =============================================
# RING3D IS JUST A SHORT TUBE
# =============================================

def RING3D(r1, r2, division = 64):
    h = 0.001
    return TUBE(r1, r2, h, division)

# =============================================
# CIRCLE 
# =============================================

def PLASM_CIRCLE (R):
    def PLASM_CIRCLE0 (subs):
        N , M = subs
        domain= PLASM_POWER([PLASM_INTERVALS(2*PI)(N), PLASM_INTERVALS(R)(M)])
        fun=lambda p: [p[1]*math.cos(p[0]),p[1]*math.sin(p[0])]
        return PLASM_MAP(fun)(domain)
    return PLASM_CIRCLE0

if self_test: 
    assert Plasm.limits(PLASM_CIRCLE(1.0)([8,8]))==Boxf(Vecf(1,-1,-1),Vecf(1,+1,+1))

# NEW DEFINITION
# English:
def CIRCLE(r, division = [64, 1]):
    if r <= 0: 
        raise ExceptionWT("Radius r in CIRCLE(r) must be positive!")
    if type(division) == list: 
        return BASEOBJ(PLASM_CIRCLE(r)(division))
    else:
        if division < 3: 
            raise ExceptionWT("Number of edges n in CIRCLE(r, n) must be at least 3!")
        return BASEOBJ(PLASM_CIRCLE(r)([division, 1]))
# Czech:
KRUH = CIRCLE
KRUZNICE = CIRCLE
# Polish:
KOLO = CIRCLE
KRAG = CIRCLE
OKRAG = CIRCLE
# German:
KREIS = CIRCLE
# Spanish:
CIRCULO = CIRCLE
# Italian:
CERCHIO = CIRCLE
# French:
CERCLE = CIRCLE
ROND = CIRCLE

def CIRCLE3D(r, division = [64, 1]):
    if r <= 0: 
        raise ExceptionWT("Radius r in CIRCLE3D(r) must be positive!")
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    if type(division) == list: 
        return PRISM(BASEOBJ(PLASM_CIRCLE(r)(division)), h)
    else:
        if division < 3: 
            raise ExceptionWT("Number of edges n in CIRCLE3D(r, n) must be at least 3!")
        return PRISM(BASEOBJ(PLASM_CIRCLE(r)([division, 1])), h)
# Czech:
KRUH3D = CIRCLE3D
# Polish:
KOLO3D = CIRCLE3D
# German:
KREIS3D = CIRCLE3D
# Spanish:
CIRCULO3D = CIRCLE3D
# Italian:
CERCHIO3D = CIRCLE3D
# French:
CERCLE3D = CIRCLE3D
ROND3D = CIRCLE3D


# =============================================
# CIRCULAR ARC 
# =============================================

def PLASM_ARC (params):
    r1, r2, angle = params
    def PLASM_ARC0 (subs):
        N , M = subs
        domain= PLASM_POWER([PLASM_INTERVALS(angle*PI/180.)(N), PLASM_INTERVALS(r2 - r1)(M)])
        fun=lambda p: [(p[1] + r1)*math.cos(p[0]), (p[1] + r1)*math.sin(p[0])]
        return PLASM_MAP(fun)(domain)
    return PLASM_ARC0

# NEW DEFINITION
# English:
def ARC(r1, r2, angle, division = [64, 1]):
    if r1 < 0: 
        raise ExceptionWT("Radius r1 in ARC(r1, r2, angle) must be nonnegative!")
    if r2 <= r1: 
        raise ExceptionWT("Radiuses r1 and r2 in ARC(r1, r2, angle) must satisfy r1 < r2!")
    if angle <= 0: 
        raise ExceptionWT("Angle in ARC(r1, r2, angle) must be positive!")
    if type(division) == list: 
        return BASEOBJ(PLASM_ARC([r1, r2, angle])(division))
    else:
        return BASEOBJ(PLASM_ARC([r1, r2, angle])([division, 1]))
# Czech
# TODO

def ARC3D(r1, r2, angle, division = [64, 1]):
    if r1 < 0: 
        raise ExceptionWT("Radius r1 in ARC3D(r1, r2, angle) must be nonnegative!")
    if r2 <= r1: 
        raise ExceptionWT("Radiuses r1 and r2 in ARC3D(r1, r2, angle) must satisfy r1 < r2!")
    if angle <= 0: 
        raise ExceptionWT("Angle in ARC3D(r1, r2, angle) must be positive!")
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    if type(division) == list: 
        return PRISM(BASEOBJ(PLASM_ARC([r1, r2, angle])(division)), h)
    else:
        return PRISM(BASEOBJ(PLASM_ARC([r1, r2, angle])([division, 1])), h)

# =============================================
# MY_CYLINDER 
# =============================================

def PLASM_MY_CYLINDER (args):
    R , H = args
    def PLASM_MY_CYLINDER0 (N):
        points=CIRCLE_POINTS(R,N)
        circle=Plasm.mkpol(2,CAT(points),[range(N)])
        return Plasm.power(circle,Plasm.mkpol(1,[0,H],[[0,1]]))
    return PLASM_MY_CYLINDER0

PLASM_CYLINDER = PLASM_MY_CYLINDER 

if self_test: 
   assert(Plasm.limits(PLASM_CYLINDER([1.0,2.0])(8)).fuzzyEqual(Boxf(Vecf(1,-1,-1,0),Vecf(1,+1,+1,2))))

# NEW DEFINITION
def CYLINDER(r, h, division = 64):
    if r <= 0: 
        raise ExceptionWT("Radius r in CYLINDER(r, h) must be positive!")
    if h <= 0: 
        raise ExceptionWT("Height h in CYLINDER(r, h) must be positive!")
    if division < 3: 
        raise ExceptionWT("Number of sides n in CYLINDER(r, h, n) must be at least 3!")
    return BASEOBJ(PLASM_CYLINDER([r, h])(division))

# English:
CYL = CYLINDER
# Czech:
VALEC = CYLINDER
# Polish:
# It is also "CYLINDER"
# German:
ZYLINDER = CYLINDER
ZYL = CYLINDER
# Spanish:
CILINDRO = CYLINDER
CIL = CYLINDER
# Italian:
CILINDRO = CYLINDER
CIL = CYLINDER
# French:
CYLINDRE = CYL

# =============================================
# SPHERE
# =============================================

def PLASM_SPHERE (radius):
    def PLASM_SPHERE0 (subds):
        N, M = subds
        domain = Plasm.translate( Plasm.power(PLASM_INTERVALS(PI)(N) , PLASM_INTERVALS(2*PI)(M)), Vecf(0, -PI/2,0 ) )
        fx  = lambda p: radius * math.cos(p[0])  * math.sin  (p[1])
        fy  = lambda p: radius * math.cos(p[0]) * math.cos (p[1])
        fz  = lambda p: radius * math.sin(p[0]) 
        ret=  PLASM_MAP([fx, fy, fz])(domain)
        return ret
    return PLASM_SPHERE0

if self_test:
	assert Plasm.limits(PLASM_SPHERE(1)([8,8])).fuzzyEqual(Boxf(Vecf(1,-1,-1,-1),Vecf(1,+1,+1,+1)))
	plasm_config.push(1e-4)
	PLASM_VIEW(PLASM_SPHERE(1)([16,16]))
	plasm_config.pop()

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def SPHERE_SURFACE(radius, divisions = [24, 48]):
    if radius <= 0: 
        raise ExceptionWT("Radius r in SPHERE_SURFACE(r) must be positive!")
    # This is a surface:
    return BASEOBJ(PLASM_SPHERE(radius)(divisions))

# English:
def SPHERE(radius, divisions = [12, 24]):
    if radius <= 0: 
        raise ExceptionWT("Radius r in SPHERE(r) must be positive!")
    divisionslist = divisions
    if not isinstance(divisions, list): 
        if divisions <= 4:
            raise ExceptionWT("Bad division in the SPHERE command!")
        divisionslist = [divisions/2, divisions]
    # Making it s solid:
    return BASEOBJ(PLASM_JOIN(PLASM_SPHERE(radius)(divisionslist)))
# Czech:
KOULE = SPHERE
# Polish:
KULA = SPHERE
SFERA = SPHERE
# German:
KUGEL = SPHERE
# Spanish:
ESFERA = SPHERE
# Italian:
SFERA = SPHERE
# French:
# Same as English

# =============================================
# TORUS - SURFACE
# =============================================

def PLASM_TORUS (radius):
    r1 , r2 = radius
    def PLASM_TORUS0 (subds):
        N , M = subds
        a=0.5*(r2-r1)
        c=0.5*(r1+r2)
        domain=Plasm.power(  PLASM_INTERVALS(2*PI)(N),  PLASM_INTERVALS(2*PI)(M)  )
        fx =   lambda p: (c+a*math.cos(p[1])) * math.cos(p[0])
        fy =   lambda p: (c+a*math.cos(p[1])) * math.sin (p[0])
        fz =   lambda p: a*math.sin(p[1])
        return PLASM_MAP(([fx,fy,fz]))(domain)
    return PLASM_TORUS0


if self_test:
   assert Plasm.limits(PLASM_TORUS([1,2])([8,8])).fuzzyEqual(Boxf(Vecf(1,-2,-2,-0.5),Vecf(1,+2,+2,+0.5)))
   plasm_config.push(1e-4)
   PLASM_VIEW(PLASM_TORUS([1,2])([20,20]))
   plasm_config.pop()

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def TORUS_SURFACE(r1, r2, divisions = [64, 32]):
    if r1 <= 0: 
        raise ExceptionWT("Inner radius r1 in TORUS_SURFACE(r1, r2) must be positive!")
    if r2 <= 0: 
        raise ExceptionWT("Outer radius r2 in TORUS_SURFACE(r1, r2) must be positive!")
    if r2 <= r1: 
        raise ExceptionWT("Inner radius r1 must be smaller than outer radius r2 in TORUS_SURFACE(r1, r2)!")
    return BASEOBJ(PLASM_TORUS([r1, r2])(divisions))

# =============================================
# TORUS - SOLID
# =============================================

def PLASM_SOLIDTORUS (radius):
    r1 , r2 = radius
    def PLASM_TORUS0 (subdomains):
        N, M, P = subdomains
        a=0.5*(r2-r1)
        c=0.5*(r1+r2)
        domain = PLASM_INSR(PLASM_PROD)([PLASM_INTERVALS(2*PI)(N), PLASM_INTERVALS(2*PI)(M), PLASM_INTERVALS(1)(P)])
        fx =   lambda p: (c + p[2]*a*math.cos(p[1])) * math.cos(p[0])
        fy =   lambda p: (c + p[2]*a*math.cos(p[1])) * math.sin(p[0])
        fz =   lambda p: p[2]*a*math.sin(p[1])
        return PLASM_MAP(([fx,fy,fz]))(domain)
    return PLASM_TORUS0

if self_test:
	PLASM_VIEW(SKELETON(1)(PLASM_SOLIDTORUS([1.5,2])([18,24,1])))

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def TORUS(r1, r2, divisions = [24, 12]):
    if r1 <= 0: 
        raise ExceptionWT("Inner radius r1 in TORUS(r1, r2) must be positive!")
    if r2 <= 0: 
        raise ExceptionWT("Outer radius r2 in TORUS(r1, r2) must be positive!")
    if r2 <= r1: 
        raise ExceptionWT("Inner radius r1 must be smaller than outer radius r2 in TORUS(r1, r2)!")
    divisionslist = divisions
    if not isinstance(divisions, list): 
        if divisions/2 <= 0:
            raise ExceptionWT("Bad division in the TORUS command!")
        divisionslist = [divisions, divisions/2]
    return BASEOBJ(PLASM_SOLIDTORUS([r1, r2])([divisionslist[0], divisionslist[1], 1]))

# English:
DONUT = TORUS
# Czech:
# It is also "TORUS"
# Polish:
# It is also "TORUS"
# German:
# It is also "TORUS"
# Spanish:
TORO = TORUS
# Italian:
# Same as in Spanish
# French:
TORE = TORUS

# =============================================
# CONE
# =============================================

def PLASM_CONE (args):
     radius , height = args
     def PLASM_CONE0(N):
        basis = PLASM_CIRCLE(radius)([N,1])
        apex = PLASM_TRANSLATE([1, 2, 3])([0, 0, height])(PLASM_SIMPLEX(0))
        return  PLASM_JOIN([basis, apex])
     return PLASM_CONE0

if self_test:
   assert Plasm.limits(PLASM_CONE([1.0,3.0])(16)).fuzzyEqual(Boxf(Vecf(1,-1,-1,0),Vecf(1,+1,+1,3)))

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def CONE(r, h, division = 64):
    if r <= 0: 
        raise ExceptionWT("Radius r in CONE(r, h) must be positive!")
    if h <= 0: 
        raise ExceptionWT("Height h in CONE(r, h) must be positive!")
    if division < 3: 
        raise ExceptionWT("Number of sides n in CONE(r, h, n) must be at least 3!")
    return BASEOBJ(PLASM_CONE([r, h])(division))

# English:
# Czech:
KUZEL = CONE
# Polish:
STOZEK = CONE
# German:
KEGEL = CONE
# Spanish:
CONO = CONE
# Italian:
# Same as in Spanish
# French:
# Same in English

# =============================================
# TRUNCONE
# =============================================

def PLASM_TRUNCONE (args):
	R1 , R2 , H = args
	def PLASM_TRUNCONE0 (N):
		domain = Plasm.power( PLASM_QUOTE([2*PI/N for i in range(N)]) , PLASM_QUOTE([1])  )
		def fn(p):
			return [
				(R1+p[1]*(R2-R1))*math.cos(p[0]),	
				(R1+p[1]*(R2-R1))*math.sin(p[0]),
				(H*p[1])
			]
		return PLASM_MAP(fn)(domain)
	return PLASM_TRUNCONE0

# NEW DEFINITION WITH NON-MANDATORY DIVISIONS:
def TRUNCONE(r1, r2, h, divisions = 64):
    if r1 <= 0: 
        raise ExceptionWT("Bottom radius r1 in TRUNCONE(r1, r2, h) must be positive!")
    if r2 <= 0: 
        raise ExceptionWT("Top radius r2 in TRUNCONE(r1, r2, h) must be positive!")
    if h <= 0: 
        raise ExceptionWT("Height h in TRUNCONE(r1, r2, h) must be positive!")
    if divisions < 3: 
        raise ExceptionWT("Number of sides n in TRUNCONE(r1, r2, h, n) must be at least 3!")
    # Changing to a solid:
    return BASEOBJ(PLASM_JOIN(PLASM_TRUNCONE([r1, r2, h])(divisions)))

# English:
TCONE = TRUNCONE
# Czech:
KOMOLYKUZEL = TRUNCONE
KKUZEL = TRUNCONE
# Polish:
SCIETYSTOZEK = TRUNCONE
SSTOZEK = TRUNCONE
# German:
KEGELSTUMPF = TRUNCONE
KSTUMPF = TRUNCONE
# Spanish:
CONOTRUNCADO = TRUNCONE
TRUNCONO = TRUNCONE
TCONO = TRUNCONE
# Italian:
TRONCONO = TRUNCONE
TCONO = TRUNCONE
# French:
TRONCONE = TCONE

# =============================================
# DODECAHEDRON
# =============================================

# This function returns an instance of BASEOBJ:
def build_DODECAHEDRON ():
	a = 1.0/(math.sqrt(3.0))
	g = 0.5*(math.sqrt(5.0)-1)
	top = MKPOL([[[1-g,1,0-g],[1+g,1,0-g]],[[1, 2]],[[1]]])
	basis = EMBED(1)(CUBOID([2, 2]))
	roof = PLASM_TRANSLATE([1, 2, 3])([-1,-1,-1])(PLASM_JOIN([basis, top]))
	roofpair = PLASM_STRUCT([roof, PLASM_ROTATE([2, 3])(PI), roof])
	geom = PLASM_S([1, 2, 3])([a, a, a])(PLASM_STRUCT([ 
		Plasm.cube(3,-1,+1),
		roofpair, 
		PLASM_R([1, 3])(PI/2), PLASM_R([1, 2])(PI/2), 
		roofpair, 
		PLASM_R([1, 2])(PI/2), PLASM_R([2, 3])(PI/2), 
		roofpair]))
        obj = BASEOBJ(geom)
        return obj

# English:
DODECAHEDRON = build_DODECAHEDRON()
# Czech:
DODEKAEDR = DODECAHEDRON
DVANACTISTEN = DODECAHEDRON
# Polish:
DWUNASTOSCIAN = DODECAHEDRON
# German:
DODEKAEDER = DODECAHEDRON
# Spanish:
DODECAEDRO = DODECAHEDRON
# Italian:
# Same as in Spanish
# French:
DODECAEDRE = DODECAHEDRON

# =============================================
# ICOSAHEDRON
# =============================================

def build_ICOSAHEDRON():
    g = 0.5*(math.sqrt(5)-1)
    b = 2.0/(math.sqrt(5*math.sqrt(5)))
    rectx = PLASM_TRANSLATE([1, 2, 3])([-g, -1, 0])(CUBOID([2*g, 2]))
    recty = PLASM_R([1, 3])(PI/2)(PLASM_R([1, 2])(PI/2)(rectx))
    rectz = PLASM_R([2, 3])(PI/2)(PLASM_R([1, 2])(PI/2)(rectx))
    geom = PLASM_S([1, 2, 3])([b, b, b])(PLASM_JOIN([rectx, recty, rectz]))
    obj = BASEOBJ(geom)
    return obj

# English:
ICOSAHEDRON = build_ICOSAHEDRON()
# Czech:
IKOSAEDR = ICOSAHEDRON
DVACETISTEN = ICOSAHEDRON
# Polish:
DWUDZIESTOSCIAN = ICOSAHEDRON
# German:
IKOSAEDER = ICOSAHEDRON
# Spanish:
ICOSAEDRO = ICOSAHEDRON
# Italian:
# Same as in Spanish
# French:
ICOSAEDRE = ICOSAHEDRON


# =============================================
# TETRAHEDRON
# =============================================

def build_TETRAHEDRON():
	return PLASM_JOIN([  PLASM_TRANSLATE([1, 2, 3])([0, 0, -1.0/3.0])(NGON(3)),  MK([0, 0, 1])  ])

PLASM_TETRAHEDRON = build_TETRAHEDRON()

def TETRAHEDRON(a, b, c, d):
    return BASEOBJ(PLASM_CONVEXHULL([a, b, c, d]))

# English:
TET = TETRAHEDRON
# Czech:
TETRAEDR = TETRAHEDRON
CTYRSTEN = TETRAHEDRON
# Polish:
CZWOROBOK = TETRAHEDRON
CZWOROSCIAN = TETRAHEDRON
# German:
TETRAEDER = TETRAHEDRON
# Spanish:
TETRAEDRO = TETRAHEDRON
# Italian:
# Same as in Spanish
# French:
TETRAEDRE = TETRAHEDRON

# =============================================
# TRIANGLE
# =============================================

def TRIANGLE(a, b, c):
    if not isinstance(a, list): 
        raise ExceptionWT("First argument a in TRIANGLE(a, b, c) must either be a 2D point [x, y] or a 3D point [x, y, z]!")
    if not isinstance(b, list): 
        raise ExceptionWT("Second argument b in TRIANGLE(a, b, c) must either be a 2D point [x, y] or a 3D point [x, y, z]!")
    if not isinstance(c, list): 
        raise ExceptionWT("Third argument c in TRIANGLE(a, b, c) must either be a 2D point [x, y] or a 3D point [x, y, z]!")
    la = len(a)
    lb = len(b)
    lc = len(c)
    if la != lb or la != lc or lb != lc:
        raise ExceptionWT("All points a, b, c in TRIANGLE(a, b, c) must be 2D points, or all must be 3D points!")
    return BASEOBJ(PLASM_CONVEXHULL([a, b, c]))

# English:
# Czech:
TROJUHELNIK = TRIANGLE
# Polish:
TROJKAT = TRIANGLE
# German:
DREIECK = TRIANGLE
# Spanish:
TRIANGULO = TRIANGLE
# Italian:
TRIANGOLO = TRIANGLE
# French:
# Same as in English

def TRIANGLE3D(a, b, c):
    if not isinstance(a, list): 
        raise ExceptionWT("First argument a in TRIANGLE3D(a, b, c) must either be a 2D point [x, y] or a 3D point [x, y, z]!")
    if not isinstance(b, list): 
        raise ExceptionWT("Second argument b in TRIANGLE3D(a, b, c) must either be a 2D point [x, y] or a 3D point [x, y, z]!")
    if not isinstance(c, list): 
        raise ExceptionWT("Third argument c in TRIANGLE3D(a, b, c) must either be a 2D point [x, y] or a 3D point [x, y, z]!")
    la = len(a)
    lb = len(b)
    lc = len(c)
    if la != lb or la != lc or lb != lc:
        raise ExceptionWT("All points a, b, c in TRIANGLE3D(a, b, c) must be 2D points, or all must be 3D points!")
    # height is kept the same for add these thin objects,
    # so that logical operations with them work:
    h = 0.001
    ## Get maximum edge length:
    #e1 = sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    #e2 = sqrt((c[0] - b[0])**2 + (c[1] - b[1])**2)
    #e3 = sqrt((c[0] - a[0])**2 + (c[1] - a[1])**2)
    #h = e1
    #if e2 > h: h = e2
    #if e3 > h: h = e3 
    # Get six points for the prism:
    a_low = [a[0], a[1], 0]
    a_high = [a[0], a[1], h]
    b_low = [b[0], b[1], 0]
    b_high = [b[0], b[1], h]
    c_low = [c[0], c[1], 0]
    c_high = [c[0], c[1], h]
    # Get the convex hull:
    return BASEOBJ(PLASM_CONVEXHULL([a_low, a_high, b_low, b_high, c_low, c_high]))
# Czech:
TROJUHELNIK3D = TRIANGLE3D
# Polish:
TROJKAT3D = TRIANGLE3D
# German:
DREIECK3D = TRIANGLE3D
# Spanish:
TRIANGULO3D = TRIANGLE3D
# Italian:
TRIANGOLO3D = TRIANGLE3D
# French:
# Same as in English


# ===================================================
# POLYPOINT 
# ===================================================

def POLYPOINT (points):
    return Plasm.mkpol( len(points[0]),CAT(points),[ [i] for i in range(len(points))] )

# ===================================================
# POLYLINE 
# ===================================================

def POLYLINE (points):
    return Plasm.mkpol( len(points[0]),CAT(points),[[i,i+1] for i in range(len(points)-1)])


# ===================================================
# TRIANGLESTRIPE 
# ===================================================

def TRIANGLESTRIPE (points):
	cells=[ [i,i+1,i+2] if (i%2==0) else [i+1,i,i+2] for i in range(len(points)-2)]
	return Plasm.mkpol(len(points[0]),CAT(points),cells)


# ===================================================
# TRIANGLEFAN 
# ===================================================

def TRIANGLEFAN (points):
	cells=[[0,i-1,i] for i in range(2,len(points))]
	return Plasm.mkpol(len(points[0]),CAT(points),cells)

# ===================================================
# MIRROR 
# ===================================================

def MIRROR (D):
    def MIRROR0 (pol):
        return  PLASM_STRUCT([PLASM_S(D)(-1)(pol),pol])
    return MIRROR0


# ===================================================
# POLYMARKER
# ===================================================

def POLYMARKER (type,MARKERSIZE=0.1):
	A,B=(MARKERSIZE,-MARKERSIZE)
	marker0=Plasm.mkpol(2,[A,0, 0,A, B,0, 0,B],[[0, 1], [1, 2], [2, 3], [3, 0]])
	marker1=Plasm.mkpol(2,[A, A, B, A, B, B, A, B], [[0, 2], [1, 3]])
	marker2=Plasm.mkpol(2,[A, A, B, A, B, B, A, B], [[0, 1], [1, 2], [2, 3], [3, 0]])
	marker3=PLASM_STRUCT([marker0,marker1])
	marker4=PLASM_STRUCT([marker0,marker2])
	marker5=PLASM_STRUCT([marker1,marker2])
	marker=[marker0, marker1, marker2, marker3, marker4,marker5][type % 6]
	def POLYMARKER_POINTS(points):
		dim=len(points[0])
		axis=range(1,dim+1)
		return Plasm.Struct([PLASM_T(axis)(point)(marker) for point in points])
	return POLYMARKER_POINTS


# ===================================================
# CHOOSE (binomial factors)
# ===================================================

def CHOOSE (args):
    N , K = args
    return FACT(N)/float(FACT(K)*FACT(N-K))

if self_test:
	assert CHOOSE([7,3])==35

# ===================================================
# TRACE
# ===================================================

def TRACE(MATRIX):
	acc=0
	dim=len(MATRIX)
	for i in range(dim):acc+=MATRIX[i][i]
	return acc

if self_test:
	assert TRACE([[5,0],[0,10]])==15

# ===================================================
# PASCALTRIANGLE
# ===================================================

def PASCALTRIANGLE (N):
	if (N==0): return [[1]]
	if (N==1): return [[1],[1,1]]
	prev=PASCALTRIANGLE(N-1)
	last_row=prev[-1]
	cur=[1]+[last_row[i-1]+last_row[i]  for i in range(1,len(last_row))] + [1]
	return prev+[cur]

if self_test:
	assert PASCALTRIANGLE(4)==[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]


# =====================================================
# see http://it.wikipedia.org/wiki/Curva_di_B%C3%A9zier
# =====================================================
def PLASM_BEZIER(U):
	def PLASM_BEZIER0 (controldata_fn):
		N=len(controldata_fn)-1

		def map_fn(point):
			t=U(point)
			controldata=[fun(point) if callable(fun) else fun for fun in controldata_fn]
			ret=[0.0 for i in range(len(controldata[0]))]		
			for I in range(N+1):
				weight=CHOOSE([N,I])*math.pow(1-t,N-I)*math.pow(t,I)
				for K in range(len(ret)):  ret[K]+=weight*(controldata[I][K])
			return ret
		return map_fn
	return PLASM_BEZIER0

if self_test:
	PLASM_VIEW(PLASM_MAP(PLASM_BEZIER(S1)([[-0,0],[1,0],[1,1],[2,1],[3,1]]))(PLASM_INTERVALS(1)(32)))
	C0 = PLASM_BEZIER(S1)([[0,0,0],[10,0,0]])
	C1 = PLASM_BEZIER(S1)([[0,2,0],[8,3,0],[9,2,0]])
	C2 = PLASM_BEZIER(S1)([[0,4,1],[7,5,-1],[8,5,1],[12,4,0]])
	C3 = PLASM_BEZIER(S1)([[0,6,0],[9,6,3],[10,6,-1]])

	plasm_config.push(1e-4)
	out = PLASM_MAP(PLASM_BEZIER(S2)([C0,C1,C2,C3]))(  Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))  )
	plasm_config.pop()
	PLASM_VIEW(out)


def PLASM_BEZIERCURVE (controlpoints):
    return PLASM_BEZIER(S1)(controlpoints)

# NEW DEFINITIONS:
def BEZIER_1(*args):
    list1 = list(args)
    if len(list1) <= 1:
        raise ExceptionWT("BEZIER curve expects at least two control points!")
    return PLASM_BEZIER(S1)(list1)

BE_1 = BEZIER_1

def BEZIER_2(*args):
    list1 = list(args)
    if len(list1) <= 1:
        raise ExceptionWT("BEZIER curve expects at least two control points!")
    return PLASM_BEZIER(S2)(list1)

BE_2 = BEZIER_2

def BEZIER_3(*args):
    list1 = list(args)
    if len(list1) <= 1:
        raise ExceptionWT("BEZIER curve expects at least two control points!")
    return PLASM_BEZIER(S3)(list1)

BE_3 = BEZIER_3


# ======================================================
# coons patch
# ======================================================

def PLASM_COONSPATCH (args):
	su0_fn , su1_fn , s0v_fn , s1v_fn = args

	def map_fn(point):
		u,v=point

		su0=su0_fn(point) if callable(su0_fn) else su0_fn
		su1=su1_fn(point) if callable(su1_fn) else su1_fn
		s0v=s0v_fn(point) if callable(s0v_fn) else s0v_fn
		s1v=s1v_fn(point) if callable(s1v_fn) else s1v_fn

		ret=[0.0 for i in range(len(su0))]	
		for K in range(len(ret)):
			ret[K]= (1-u)*s0v[K]+u*s1v[K]+(1-v)*su0[K]+v*su1[K]+(1-u)*(1-v)*s0v[K]+(1-u)*v*s0v[K]+u*(1-v)*s1v[K]+u*v*s1v[K] 
		return ret
	return map_fn


if self_test:
	Su0=PLASM_BEZIER(S1)([[0,0,0],[10,0,0]])
	Su1=PLASM_BEZIER(S1)([[0,10,0],[2.5,10,3],[5,10,-3],[7.5,10,3],[10,10,0]])
	Sv0=PLASM_BEZIER(S2)([[0,0,0],[0,0,3],[0,10,3],[0,10,0]])
	Sv1=PLASM_BEZIER(S2)([[10,0,0],[10,5,3],[10,10,0]])
	plasm_config.push(1e-4)
	out=PLASM_MAP(PLASM_COONSPATCH([Su0,Su1,Sv0,Sv1]))(Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10)))
	plasm_config.pop()
	PLASM_VIEW(out)

# NEW DEFINITION:
def COONSPATCH(a, b, c, d):
    return PLASM_COONSPATCH([a, b, c, d])

# ======================================================
# RULED SURFACE
# ======================================================

def PLASM_RULEDSURFACE (args):
	alpha_fn , beta_fn = args

	def map_fn(point):
		u,v=point
		alpha,beta=alpha_fn(point),beta_fn(point)
		ret=[0.0 for i in range(len(alpha))]	
		for K in range(len(ret)): ret[K]=alpha[K]+v*beta[K]
		return ret
	return map_fn


if self_test:
	alpha= lambda point: [point[0],point[0],       0 ]
	beta = lambda point: [      -1,      +1,point[0] ]
	domain= PLASM_TRANSLATE([1, 2, 3])([-1, -1, 0])(Plasm.power(PLASM_INTERVALS(2)(10),PLASM_INTERVALS(2)(10)))
	plasm_config.push(1e-4)
	PLASM_VIEW(PLASM_MAP(PLASM_RULEDSURFACE([alpha,beta]))(domain))
	plasm_config.pop()

# NEW DEFINITION
def RULED_SURFACE(a, b):
    return PLASM_RULEDSURFACE([a, b])
RUSURFACE = RULED_SURFACE
RUS = RULED_SURFACE
    
# ======================================================
# PROFILE SURFACE
# ======================================================

def PROFILEPRODSURFACE (args):
	profile_fn,section_fn = args

	def map_fun(point):
		u,v=point
		profile,section=profile_fn(point),section_fn(point)
		ret=[profile[0]*section[0],profile[0]*section[1],profile[2]]
		return ret
	return map_fun

if self_test:
	alpha=PLASM_BEZIER(S1)([[0.1,0,0],[2,0,0],[0,0,4],[1,0,5]])
	beta =PLASM_BEZIER(S2)([[0,0,0],[3,-0.5,0],[3,3.5,0],[0,3,0]])
	plasm_config.push(1e-4)
	domain=Plasm.power(PLASM_INTERVALS(1)(20),PLASM_INTERVALS(1)(20))
	out=Plasm.Struct([PLASM_MAP(alpha)(domain),PLASM_MAP(beta )(domain),PLASM_MAP(PROFILEPRODSURFACE([alpha,beta]))(domain)])
	plasm_config.pop()
	PLASM_VIEW(out)

# NEW DEFINITION
def PROFILE_PROD_SURFACE(a, b):
    return PROFILEPRODSURFACE([a, b])
PPSURFACE = PROFILE_PROD_SURFACE

    
# ======================================================
# ROTATIONALSURFACE
# ======================================================

def ROTATIONALSURFACE (args):
	profile = args

	def map_fn(point):
		u,v=point
		f,h,g= profile(point)
		ret=[f*math.cos(v),f*math.sin(v),g]
		return ret
	return map_fn

if self_test:
	profile=PLASM_BEZIER(S1)([[0,0,0],[2,0,1],[3,0,4]]) # defined in xz!
	plasm_config.push(1e-4)
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(2*PI)(30)) # the first interval should be in 0,1 for bezier
	out=PLASM_MAP(ROTATIONALSURFACE(profile))(domain)
	plasm_config.pop()
	PLASM_VIEW(out)

# NEW COMMAND:
def ROTATIONAL_SURFACE(args):
    return ROTATIONALSURFACE(args)
ROSURFACE = ROTATIONAL_SURFACE
ROS = ROTATIONAL_SURFACE

    
# ======================================================
# CYLINDRICALSURFACE
# ======================================================

def CYLINDRICALSURFACE (args):
	alpha_fun   = args[0]
	beta_fun    = CONS(AA(K)(args[1]))
	return PLASM_RULEDSURFACE([alpha_fun,beta_fun])

if self_test:
	alpha=PLASM_BEZIER(S1)([[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0]])
	Udomain=PLASM_INTERVALS(1)(20)
	Vdomain=PLASM_INTERVALS(1)(6)
	domain=Plasm.power(Udomain,Vdomain)
	fn=CYLINDRICALSURFACE([alpha,[0,0,1]])
	PLASM_VIEW(PLASM_MAP(fn)(domain))

# NEW COMMAND:
def CYLINDRICAL_SURFACE(a, b):
    return CYLINDRICALSURFACE([a, b])
CYSURFACE = CYLINDRICAL_SURFACE


# ======================================================
# CONICALSURFACE
# ======================================================

   
def CONICALSURFACE (args):
	apex=args[0]
	alpha_fn   = lambda point: apex
	beta_fn    = lambda point: [ args[1](point)[i]-apex[i] for i in range(len(apex))]
	return PLASM_RULEDSURFACE([alpha_fn, beta_fn])


if self_test:
	domain=Plasm.power(PLASM_INTERVALS(1)(20),PLASM_INTERVALS(1)(6))
	beta=PLASM_BEZIER(S1)([ [1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0] ])
	out=PLASM_MAP(CONICALSURFACE([[0,0,1],beta]))(domain)
	PLASM_VIEW(out)

# NEW COMMAND:
def CONICAL_SURFACE(a, b):
    return CONICALSURFACE([a, b])
COSURFACE = CONICAL_SURFACE


# ======================================================
# CUBICHERMITE
# ======================================================

def PLASM_CUBICHERMITE (U):
	def PLASM_CUBICHERMITE0 (args):
		p1_fn , p2_fn , s1_fn , s2_fn = args
		def map_fn(point):
			u=U(point);u2=u*u;u3=u2*u
			p1,p2,s1,s2=[f(point) if callable(f) else f for f in [p1_fn , p2_fn , s1_fn , s2_fn]]
			ret=[0.0 for i in range(len(p1))]		
			for i in range(len(ret)):				
				ret[i]+=(2*u3-3*u2+1)*p1[i] + (-2*u3+3*u2)*p2[i]+(u3-2*u2+u)*s1[i]+(u3-u2)*s2[i]
			return ret
		return map_fn
	return PLASM_CUBICHERMITE0

if self_test:

	domain=PLASM_INTERVALS(1)(20)
	out=Plasm.Struct([
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[ -1, 1],[ 1,0]]))(domain),
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[ -2, 2],[ 2,0]]))(domain),
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[ -4, 4],[ 4,0]]))(domain),
		PLASM_MAP(PLASM_CUBICHERMITE(S1)([[1,0],[1,1],[-10,10],[10,0]]))(domain)
	])
	PLASM_VIEW(out)

	c1=PLASM_CUBICHERMITE(S1)([[1  ,0,0],[0  ,1,0],[0,3,0],[-3,0,0]])
	c2=PLASM_CUBICHERMITE(S1)([[0.5,0,0],[0,0.5,0],[0,1,0],[-1,0,0]])
	sur3=PLASM_CUBICHERMITE(S2)([c1,c2,[1,1,1],[-1,-1,-1]])
	plasm_config.push(1e-4)
	domain=Plasm.power(PLASM_INTERVALS(1)(14),PLASM_INTERVALS(1)(14))
	out=PLASM_MAP(sur3)(domain)
	plasm_config.pop()
	PLASM_VIEW(out)

# NEW DEFINITION
def CUBIC_HERMITE_1(*args):
    return PLASM_CUBICHERMITE(S1)(list(args))

CH_1 = CUBIC_HERMITE_1

def CUBIC_HERMITE_2(*args):
    return PLASM_CUBICHERMITE(S2)(list(args))

CH_2 = CUBIC_HERMITE_2

def CUBIC_HERMITE_3(*args):
    return PLASM_CUBICHERMITE(S3)(list(args))

CH_3 = CUBIC_HERMITE_3

def PLASM_HERMITE(args):
    P1 , P2 , T1 , T2 = args
    return PLASM_CUBICHERMITE(S1)([P1, P2, T1, T2])




# ======================================================
# EXTRUDE
# ======================================================
#
#def Q(H):
#	return Plasm.mkpol(1,[0,H],[[0,1]])
#
#def PLASM_EXTRUDE (args):
#	__N, Pol, H = args
#	return Plasm.power(Pol,Q(H))
#
# NEW DEFINITION (ALLOWS OMITTING BRACKETS)
#def EXTRUDE(*args):
#    return PLASM_EXTRUDE(list(args))
#
#def MULTEXTRUDE (P):
#	def MULTEXTRUDE0 (H):
#		return Plasm.power(P,Q(H))
#	return MULTEXTRUDE0
#

# ======================================================
# PROJECT
# ======================================================

def PROJECT (M):
	def PROJECT0 (POL):
		vertices,cells,pols=UKPOL(POL)
		vertices=[vert[0:-M] for vert in vertices]
		return MKPOL([vertices,cells,pols])
	return PROJECT0



# ======================================================
# SPLITCELLS
# ======================================================

def SPLITCELLS (scene):
	vertices,cells,pols= UKPOL(scene)
	ret=[]
	for c in cells: ret+=[MKPOL([vertices,[c],[[1]]])]
	return ret


def EXTRACT_WIRES (scene):
    return SPLITCELLS(SKEL_1(scene))

# no notion of pols for xge mkpol!
SPLITPOLS=SPLITCELLS

# ===================================================
# PERMUTATIONS
# ===================================================

def PERMUTATIONS (SEQ):
	if len(SEQ)<=1: return [SEQ]
	ret=[]
	for i in range(len(SEQ)):
		element =SEQ[i]
		rest    =PERMUTATIONS(SEQ[0:i] + SEQ[i+1:])
		for r in rest: ret+=[[element] + r]
	return ret
	
if self_test:
	assert len(PERMUTATIONS([1,2,3]))==6


# ===================================================
# PERMUTAHEDRON
# ===================================================

def PERMUTAHEDRON (d):
	vertices = PERMUTATIONS(range(1,d+2))
	center = MEANPOINT(vertices)
	cells=[range(1,len(vertices)+1)]
	object=MKPOL([vertices,cells,[[1]]])
	object=Plasm.translate(object,Vecf([0] + center)*-1)
	for i in range(1,d+1): object=PLASM_R([i,d+1])(PI/4)(object)
	object=PROJECT(1)(object)
	return object


if self_test:
	PLASM_VIEW(Plasm.Struct([PERMUTAHEDRON(2),SKEL_1(PERMUTAHEDRON(2))]))
	PLASM_VIEW(Plasm.Struct([PERMUTAHEDRON(3),SKEL_1(PERMUTAHEDRON(3))]))



# ===================================================
# STAR
# ===================================================

from numpy import tan

def STAR (r, n):
    if n < 5: raise ExceptionWT("In the STAR(r, n) command, n must be at least 5!")
    if r <= 0: raise ExceptionWT("In the STAR(r, n) command, the radius r must be positive!")
    beta = 2.*PI/n
    x = r / tan(beta)
    t0 = TRIANGLE([-x, 0], [x, 0], [0, r])
    l1 = [t0]
    angle = 360./n
    for i in range(n-1):
        l1.append(R(COPY(t0), (i+1) * angle))
    return U(l1)


# ===================================================
# SCHLEGEL
# ===================================================

def SCHLEGEL2D(D):
	def map_fn(point):
		return [D*point[0]/point[2],D*point[1]/point[2]]
	return PLASM_MAP(map_fn)

def SCHLEGEL3D (D):
	def map_fn(point):
		return [D*point[0]/point[3],D*point[1]/point[3],D*point[2]/point[3]]
	return PLASM_MAP(map_fn)


if self_test:
	PLASM_VIEW(SCHLEGEL3D(0.2)(SKEL_1(PLASM_T([1,2,3,4])([-1.0/3.0,-1.0/3.0,-1,+1])(PLASM_SIMPLEX(4)))))
	PLASM_VIEW(SCHLEGEL3D(0.2)(SKEL_1(PLASM_T([1,2,3,4])([-1,-1,-1,1])(CUBOID([2,2,2,2])))))
	PLASM_VIEW(SCHLEGEL3D(0.2)(SKEL_1(PLASM_T([1,2,3,4])([-1.0/3.0,-1.0/3.0,-1,+1])(Plasm.power(PLASM_SIMPLEX(2),PLASM_SIMPLEX(2))))))

# ===================================================
# FINITECONE
# ===================================================

def FINITECONE (pol):
	point=[0 for i in range(RN(pol))]
	return PLASM_JOIN([pol,MK(point)])


# ===================================================
# PRISM
# ===================================================

def PLASM_PRISM (height):
    def PLASM_PRISM0 (basis):
        return Plasm.power(basis, PLASM_QUOTE([height]))
    return PLASM_PRISM0

# NEW DEFINITION - RETURNS AN INSTANCE OF CLASS "PRODUCT" OR A LIST
# OF PRODUCTS:
def PRISM(basis, h):
    if h <= 0: 
        raise ExceptionWT("Height in PRISM(base, height) must be positive!")
    # Check that the basis is two-dimensional:
    if not isinstance(basis, list):
        if basis.dim <> 2: 
            raise ExceptionWT("The base object in PRISM(base, height) must be 2-dimensional!")
        color = basis.getcolor()
        obj = PRODUCT(basis, GRID(h))  # PRODUCT returns a class instance!
        obj.setcolor(color)
        return obj
    else:
        basis = flatten(basis)
        for obj in basis:
            if obj.dim <> 2: 
                raise ExceptionWT("The base object in PRISM(base, height) must be 2-dimensional!") 
        obj = []
        for oo in basis:
            color = oo.getcolor()
            oo3d = PRODUCT(oo, GRID(h))  # PRODUCT returns a class instance!
            oo3d.setcolor(color)
            obj.append(oo3d)
        return obj
     
# English:
# Czech:
HRANOL = PRISM
# Polish:
PRYZMA = PRISM
PRYZMAT = PRISM
# German:
PRISMA = PRISM
# Spanish:
# Same as in German
# Italian:
# Same as in German
# French:
PRISME = PRISM

# ===================================================
# CROSSPOLYTOPE
# ===================================================

def CROSSPOLYTOPE (D):
	points=[]
	for i in range(D):
		point_pos=[0 for x in range(D)];point_pos[i]=+1
		point_neg=[0 for x in range(D)];point_neg[i]=-1
		points+=[point_pos,point_neg]

	cells=[range(1,D*2+1)]
	pols=[[1]]
	return MKPOL([points,cells,pols])

OCTAHEDRON = CROSSPOLYTOPE(2)
OKTAEDR = OCTAHEDRON
OCTAEDER = OCTAHEDRON
OCTAEDRO = OCTAHEDRON

# ===================================================
# MATHOM
# ===================================================

def MATHOM (M):
	return [[1] + [0 for i in range(len(M))]] + map(lambda l: [0]+l, M)

if self_test:
	assert MATHOM([[1,2],[3,4]])==[[1,0,0],[0,1,2],[0,3,4]]



# ===================================================
# ROTN
# ===================================================

def ROTN (args):
	alpha, N = args
	N=UNITVECT(N)
	QX = UNITVECT((VECTPROD([[0, 0, 1],N])))

	QZ = UNITVECT(N)
	QY = VECTPROD([QZ,QX])
	Q  = MATHOM([QX, QY, QZ])

	ISUP = COMP([AND, CONS([COMP([C(EQ)(0), S1]), COMP([C(EQ)(0), S2]), COMP([COMP([NOT, C(EQ)(0)]), S3])])])

	if N[0]==0 and N[1]==0:
		return PLASM_R([1, 2])(alpha)
	else:
		return COMP([MAT(TRANS(Q)),PLASM_R([1, 2])(alpha),MAT(Q)])


# ===================================================
# MKVECTOR
# ===================================================

def MKVECTOR (P1):
    def MKVECTOR0 (P2):
        TR = PLASM_T([1, 2, 3])(P1)
        U = VECTDIFF([P2,P1])
        ALPHA = ACOS((INNERPROD([[0, 0, 1],UNITVECT(U)])))
        B = VECTNORM(U)
        SC = PLASM_S([1, 2, 3])([B, B, B])
        N = VECTPROD([[0, 0, 1],U])
        ROT = ROTN([ALPHA, N])
        return (COMP([COMP([TR, ROT]), SC]))(MKVERSORK)
    return MKVECTOR0


# ===================================================
# Matrix stuff
# ===================================================

SCALARMATPROD = COMP([COMP([(COMP([AA, AA]))(RAISE(PLASM_PROD)), AA(DISTL)]), DISTL])

MATDOTPROD = COMP([INNERPROD, AA(CAT)])

def ORTHO (matrix):
	return SCALARMATPROD([0.5,PLASM_SUM([matrix,TRANS(matrix)])])

def SKEW (matrix):
    return SCALARMATPROD([0.5, PLASM_DIFF([matrix,TRANS(matrix)])])


if self_test:
	temp=[[1,2],[3,4]]
	assert SCALARMATPROD([10.0,temp])==[[10,20],[30,40]]
	assert MATDOTPROD([temp,[[1,0],[0,1]]])==5
	assert ORTHO([[1,0],[0,1]])==[[1,0],[0,1]]
	assert SKEW ([[1,0],[0,1]])==[[0,0],[0,0]]



# ======================================================
# CUBICUBSPLINE
# ======================================================

def CUBICUBSPLINE (domain):
	
	def CUBICUBSPLINE0(args):
		q1_fn, q2_fn , q3_fn , q4_fn = args


		def map_fn(point):
			u=S1(point)
			u2=u*u
			u3=u2*u
			q1,q2,q3,q4=[f(point) if callable(f) else f for f in [q1_fn,q2_fn,q3_fn,q4_fn]]
			ret=[0 for x in range(len(q1))]
			for i in range(len(ret)):
				ret[i]=(1.0/6.0)*  ( (-u3+3*u2-3*u+1)*q1[i] + (3*u3-6*u2+4)*q2[i]  + (-3*u3+3*u2+3*u+1)*q3[i] + (u3)*q4[i]  )
			return ret
		return PLASM_MAP(map_fn)(domain)
	return CUBICUBSPLINE0



# ===========================================
# CUBICCARDINAL
# ===========================================

def CUBICCARDINAL (domain,h=1):
	def CUBICCARDINAL0(args):
		q1_fn , q2_fn , q3_fn , q4_fn = args
		def map_fn(point):
			u=S1(point)
			u2=u*u
			u3=u2*u
			q1,q2,q3,q4=[f(point) if callable(f) else f for f in [q1_fn,q2_fn,q3_fn,q4_fn]]
			
			ret=[0.0 for i in range(len(q1))]	
			for i in range(len(ret)):
				ret[i]=(-h*u3+2*h*u2-h*u)*q1[i] +((2-h)*u3+(h-3)*u2+1)*q2[i] + ((h-2)*u3+(3-2*h)*u2+h*u)*q3[i] + (h*u3-h*u2)*q4[i]

			return ret
		return PLASM_MAP(map_fn)(domain)
	return CUBICCARDINAL0


# ======================================================
# SPLINE
# ======================================================

def SPLINE (curve):
	def SPLINE0(points):
		ret=[]
		for i in range(len(points)-4+1):
			P=points[i:i+4]
			ret+=[curve(P)]
		return Plasm.Struct(ret)
	return SPLINE0



if self_test:
	domain=PLASM_INTERVALS(1)(20)
	points = [[-3,6],[-4,2],[-3,-1],[-1,1],[1.5,1.5],[3,4],[5,5],[7,2],[6,-2],[2,-3]]
	PLASM_VIEW(SPLINE(CUBICCARDINAL(domain))(points))
	PLASM_VIEW(SPLINE(CUBICUBSPLINE(domain))(points))

# ======================================================
# CUBICUBSPLINE
# ======================================================

def JOINTS (curve):
	knotzero = MK([0])
	def JOINTS0(points):
		points,cells,pols=UKPOL(SPLINE(curve(knotzero)))
		return POLYMARKER(2)(points)



# ======================================================
# BERNSTEINBASIS
# ======================================================

def BERNSTEINBASIS (U):
	def BERNSTEIN0 (N):
		def BERNSTEIN1 (I):

			def map_fn(point):

				t=U(point)
				ret=CHOOSE([N,I])*math.pow(1-t,N-I)*math.pow(t,I)
				return ret
			return map_fn
		return [BERNSTEIN1(I) for I in range(0,N+1)]
	return BERNSTEIN0


# ======================================================
# TENSORPRODSURFACE
# ======================================================

def TENSORPRODSURFACE (args):
	ubasis , vbasis = args
	def TENSORPRODSURFACE0 (controlpoints_fn):

		def map_fn(point):

			# resolve basis
			u,v=point
			U=[f([u]) for f in ubasis]
			V=[f([v]) for f in vbasis]
			
			controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

			# each returned vector will be this side (the tensor product is SOLID)
			target_dim=len(controlpoints[0][0])

			ret=[0 for x in range(target_dim)]
			for i in range(len(ubasis)):
				for j in range(len(vbasis)):
					for M in range(len(ret)):
						for M in range(target_dim): 
							ret[M]+= U[i]*V[j] * controlpoints[i][j][M]

			return ret
		return map_fn
	return TENSORPRODSURFACE0

# ======================================================
# BILINEARSURFACE
# ======================================================

def BILINEARSURFACE(controlpoints):
	return TENSORPRODSURFACE([BERNSTEINBASIS(S1)(1),BERNSTEINBASIS(S1)(1)])(controlpoints)

if self_test:
	controlpoints=[[[0,0,0],[2,-4,2]],[[0,3,1],[4,0,0]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=BILINEARSURFACE(controlpoints)
	PLASM_VIEW(PLASM_MAP(mapping)(domain))

# ======================================================
# BIQUADRATICSURFACE
# ======================================================

def BIQUADRATICSURFACE (controlpoints):
	def u0(point):u=S1(point);return 2*u*u-u
	def u1(point):u=S1(point);return 4*u-4*u*u
	def u2(point):u=S1(point);return 2*u*u-3*u+1
	basis = [u0, u1, u2]
	return TENSORPRODSURFACE([basis, basis])(controlpoints)

if self_test:
	controlpoints=[[[0,0,0],[2,0,1],[3,1,1]],[[1,3,-1],[3,2,0],[4,2,0]],[[0,9,0],[2,5,1],[3,3,2]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=BIQUADRATICSURFACE(controlpoints)
	plasm_config.push(1e-4)
	PLASM_VIEW(PLASM_MAP(mapping)(domain))
	plasm_config.pop()


# ======================================================
# HERMITESURFACE
# ======================================================

def PLASM_HERMITESURFACE(controlpoints):
	def H0(point):u=S1(point);u2=u*u;u3=u2*u;return u3-u2
	def H1(point):u=S1(point);u2=u*u;u3=u2*u;return u3-2*u2+u
	def H2(point):u=S1(point);u2=u*u;u3=u2*u;return 3*u2-2*u3
	def H3(point):u=S1(point);u2=u*u;u3=u2*u;return 2*u3-3*u2+1
	basis=[H3, H2, H1, H0]
	return  TENSORPRODSURFACE([basis, basis])(controlpoints)

if self_test:
	controlpoints=[[[0,0,0 ],[2,0,1],[3,1,1],[4,1,1]],[[1,3,-1],[3,2,0],[4,2,0],[4,2,0]],[[0,4,0 ],[2,4,1],[3,3,2],[5,3,2]],[[0,6,0 ],[2,5,1],[3,4,1],[4,4,0]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=PLASM_HERMITESURFACE(controlpoints)
	plasm_config.push(1e-4)
	PLASM_VIEW(PLASM_MAP(mapping)(domain))
	plasm_config.pop()

# ======================================================
# PLASM_BEZIERSURFACE
# ======================================================

def PLASM_BEZIERSURFACE (controlpoints):
    M = len(controlpoints   )-1
    N = len(controlpoints[0])-1
    return TENSORPRODSURFACE([BERNSTEINBASIS(S1)(M), BERNSTEINBASIS(S1)(N)])(controlpoints)

if self_test:
	controlpoints=[
		[[ 0,0,0],[0 ,3  ,4],[0,6,3],[0,10,0]],
		[[ 3,0,2],[2 ,2.5,5],[3,6,5],[4,8,2]],
		[[ 6,0,2],[8 ,3 , 5],[7,6,4.5],[6,10,2.5]],
		[[10,0,0],[11,3  ,4],[11,6,3],[10,9,0]]]
	domain=Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))
	mapping=PLASM_BEZIERSURFACE(controlpoints)
	plasm_config.push(1e-4)
	PLASM_VIEW(PLASM_MAP(mapping)(domain))
	plasm_config.pop()

# ======================================================
# generic tensor product
# ======================================================

def TENSORPRODSOLID (args):
	# todo other cases (>3 dimension!)
	ubasis,vbasis,wbasis = args
	def TENSORPRODSOLID0 (controlpoints_fn):

		def map_fn(point):

			# resolve basis
			u,v,w=point
			U=[f([u]) for f in ubasis]
			V=[f([v]) for f in vbasis]
			W=[f([w]) for f in wbasis]

			# if are functions call them
			controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

			# each returned vector will be this side (the tensor product is SOLID)
			target_dim=len(controlpoints[0][0][0])

			# return vector
			ret=[0 for x in range(target_dim)]
			for i in range(len(ubasis)):
				for j in range(len(vbasis)):
					for k in range(len(wbasis)):
						for M in range(target_dim): 
							ret[M]+= U[i]*V[j]*W[k] * controlpoints[M][i][j][k]
			return ret

		return map_fn
	return TENSORPRODSOLID0

# ======================================================
# PLASM_BEZIERMANIFOLD
# ======================================================

def PLASM_BEZIERMANIFOLD (degrees):
	basis=[BERNSTEINBASIS(S1)(d) for d in degrees]
	return TENSORPRODSOLID(basis)

if self_test:
	grid1D = PLASM_INTERVALS(1)(5)
	domain3D = Plasm.power(Plasm.power(grid1D,grid1D),grid1D)
	degrees = [2,2,2]
	Xtensor =  [[[0,1,2],[-1,0,1],[0,1,2]],[[0,1,2],[-1,0,1],[0,1,2]],[[0,1,2],[-1,0,1],[0,1,2]]]
	Ytensor =  [[[0,0,0.8],[1,1,1],[2,3,2]],[[0,0,0.8],[1,1,1],[2,3,2]],[[0,0,0.8],[1,1,1],[2,3,2]]]
	Ztensor =  [[[0,0,0],[0,0,0],[0,0,0]],[[1,1,1],[1,1,1],[1,1,1]],[[2,2,1],[2,2,1],[2,2,1]]] 
	mapping = PLASM_BEZIERMANIFOLD(degrees)([Xtensor,Ytensor,Ztensor])
	out=PLASM_MAP(mapping)(domain3D)
	PLASM_VIEW(out)

# ===================================================
# LOCATE
# ===================================================

def LOCATE (args):
	pol, a, distances = args
	ret=[]
	for d in distances:
		ret+=[PLASM_T(a)(d),pol]
	return PLASM_STRUCT(ret)


# ===================================================
# SUBSEQ
# ===================================================

def SUBSEQ (I_J):
	def SUBSEQ0 (SEQ):
		return SEQ[I_J[0]-1:I_J[1]]
	return SUBSEQ0



# ===================================================
# NORTH,SOUTH,WEST,EAST
# ===================================================

NORTH    = CONS([CONS([MAX(1), MAX(2)]), CONS([MIN(1), MIN(2)])])
SOUTH    = CONS([CONS([MIN(1), MIN(2)]), CONS([MAX(1), MIN(2)])])
WEST     = CONS([CONS([MIN(1), MAX(2)]), CONS([MIN(1), MIN(2)])])
EAST     = CONS([CONS([MAX(1), MIN(2)]), CONS([MAX(1), MAX(2)])])

MXMY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), MID([1, 2])]), ID])])
MXBY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MID(1), MIN(2)])]), ID])])
MXTY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MID(1), MAX(2)])]), ID])])
LXMY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MIN(1), MID(2)])]), ID])])
RXMY = COMP([PLASM_STRUCT, CONS([COMP([COMP([PLASM_T([1, 2]), AA(RAISE( PLASM_DIFF))]), CONS([MAX(1), MID(2)])]), ID])])


# ===================================================
# RIF
# ===================================================

def RIF (size):
	thin = 0.01*size
	x=PLASM_COLOR(RED)(CUBOID([size, thin, thin]))
	y=PLASM_COLOR(GREEN)(CUBOID([thin, size, thin]))
	z=PLASM_COLOR(BLUE)(CUBOID([thin, thin, size]))
	return Plasm.Struct([x,y,z])




# ===================================================
# FRACTALSIMPLEX
# ===================================================

def FRACTALSIMPLEX (D):
    def FRACTALSIMPLEX0 (N):

		mkpols = COMP([COMP([COMP([COMP([PLASM_STRUCT, AA(MKPOL)]), AA(AL)]), DISTR]), CONS([ID, K([[FROMTO([1,D+1])], [[1]]])])])

		def COMPONENT (args):
			i, seq = args
			firstseq =   seq[0:i-1]
			pivot    = seq[i-1]
			lastseq = seq[i:len(seq)]
			firstpart = AA(MEANPOINT)(DISTR([firstseq, pivot]))
			lastpart  = AA(MEANPOINT)(DISTR([lastseq , pivot]))
			return CAT([firstpart, [pivot], lastpart])

		expand = COMP([COMP([AA(COMPONENT), DISTR]), CONS([COMP([INTSTO, LEN]), ID])])
		splitting = (COMP([COMP, DIESIS(N)]))((COMP([CAT, AA(expand)])))
	
		return (COMP([COMP([COMP([COMP([mkpols, splitting]), CONS([S1])])])]))(UKPOL(PLASM_SIMPLEX(D)))

    return FRACTALSIMPLEX0


# ===================================================
# VECT2MAT
# ===================================================

def VECT2MAT(v):
	n=len(v)
	return [[0 if r!=c else v[r] for c in range(n)] for r in range(n)]
	

# ===================================================
# VECT2DTOANGLE
# ===================================================

def VECT2DTOANGLE(v):
	v=UNITVECT(v)
	return math.acos(v[0])*(1 if v[1]>=0 else -1)


# ===================================================
# CART
# ===================================================

def CART(l):
    CART2 = COMP([COMP([CAT, AA(DISTL)]), DISTR])
    F1 = AA((AA(CONS([ID]))))
    return TREE(COMP([AA(CAT), CART2]))(F1(l))


def POWERSET(l):
	return COMP([COMP([AA(CAT), CART]), AA((CONS([CONS([ID]), K([])])))])(l)


if self_test:
	assert len(CART([[1, 2, 3], ['a', 'b'],[10,11]]))==12
	assert len(POWERSET([ 1, 2, 3]) )==8



# ===================================================
# ARC - OLD
# ===================================================

#def ARC(args):
#	degrees , cents = args
#	return PI*(degrees+cents)/(100.0*180.0)


# ===================================================
# PYRAMID
# ===================================================


def PYRAMID (H):
	def PYRAMID0(pol):
		barycenter=MEANPOINT(UKPOL(pol)[0])
		return PLASM_JOIN([MK(barycenter+[H]),pol])
	return PYRAMID0


# ===================================================
# MESH
# ===================================================

def MESH (seq):
	return INSL(RAISE(PLASM_PROD))([PLASM_QUOTE(i) for i in seq])



# ===================================================
# NU_GRID
# ===================================================

def NU_GRID (data):
	polylines=[POLYLINE(i) for i in data]
	return INSL(RAISE(PLASM_PROD))(polylines)



# ===================================================
# CURVE2PLASM_MAPVECT
# ===================================================

def CURVE2PLASM_MAPVECT (CURVE):
	D = len((CURVE([0])))
	return [ COMP([SEL(i),CURVE]) for i in FROMTO([1,D]) ]

if self_test:
	temp=CURVE2PLASM_MAPVECT(lambda t: [t[0]+1,t[0]+2])
	assert temp[0]([10])==11
	assert temp[1]([10])==12


# ===================================================
# SEGMENT
# ===================================================

def SEGMENT (sx):
	def SEGMENT0 (args):
		N=len(args[0])
		A,B=args
		P0=A
		P1=[A[i]+(B[i]-A[i])*sx for i in range(N)]

		print P0,P1
		return POLYLINE([P0,P1])
	return SEGMENT0

# ===================================================
# SOLIDIFY
# ===================================================

def SOLIDIFY(pol):
	
	box=Plasm.limits(pol)
	min=box.p1[1]
	max=box.p2[1]
	siz=max-min
	far_point=max+siz*100

	def InftyProject(pol):
		verts,cells,pols=UKPOL(pol)
		verts=[[far_point] + v[1:] for v in verts]
		return MKPOL([verts,cells,pols])

	def IsFull(pol):
		return PLASM_DIM(pol)==RN(pol)

	ret=SPLITCELLS(pol)
	ret=[PLASM_JOIN([pol,InftyProject(pol)]) for pol in ret]
	return PLASM_XOR(FILTER(IsFull)(ret))

if self_test:

	PLASM_VIEW(SOLIDIFY(PLASM_STRUCT(AA(POLYLINE)([
		[[0,0],[4,2],[2.5,3],[4,5],[2,5],[0,3],[-3,3],[0,0]],
		[[0,3],[0,1],[2,2],[2,4],[0,3]],
		[[2,2],[1,3],[1,2],[2,2]]]))))

# ===================================================
# PLASM_EXTRUSION - ONE PIECE IN THE VERTICAL DIRECTION
# ===================================================

def PLASM_EXTRUSION (angle):
	def PLASM_EXTRUSION1 (height):
		def PLASM_EXTRUSION0 (pol):
			dim = PLASM_DIM(pol)
			cells=SPLITCELLS( SKELETON(dim)(pol) )
			slice=[EMBED(1)(c) for c in cells]
			tensor=COMP([PLASM_T(dim+1)(1.0/height),PLASM_R([dim-1,dim])(angle/height)])
			layer=Plasm.Struct([PLASM_JOIN([p,tensor(p)]) for p in slice])
			return (COMP([COMP([PLASM_STRUCT, CAT]), DIESIS(height)]))([layer, tensor])
		return PLASM_EXTRUSION0
	return PLASM_EXTRUSION1

# ===================================================
# EXTRUSION - WITH ARBITRATRY DIVISION IN VERTICAL DIRECTION
# ===================================================

def EXTRUDEONE(shape2d, height, angle_deg, n=1):
  if shape2d.dim <> 2:
      raise ExceptionWT("Base object in EXTRUDE(...) must be 2-dimensional!")
  if height <= 0:
      raise ExceptionWT("Extrusion height in EXTRUDE(...) must be positive!")
  col = shape2d.getcolor()
  dh = float(height) / n
  angle_rad = angle_deg * PI / 180.0
  da = float(angle_rad) / n
  dangle = da*180.0/PI
  L = []
  for i in range(0, n):
    newlayer = BASEOBJ(PLASM_EXTRUSION(da)(1)(shape2d.geom))
    COLOR(newlayer, col)
    S(newlayer, 1, 1, dh)
    MOVE(newlayer, 0, 0, i * dh)
    ROTATE(newlayer, i * dangle, 3)
    L.append(newlayer)
  return L # I tried to return a union but it took too much time

def EXTRUDE(basis, height, angle_deg, n=1):
    if height <= 0: 
        raise ExceptionWT("Height in EXTRUDE(base, height, angle, n) must be positive!")
    # Check that the basis is two-dimensional:
    if not isinstance(basis, list):
        if basis.dim <> 2: 
            raise ExceptionWT("The base object in EXTRUDE(base, height, angle, n) must be 2-dimensional!")
        color = basis.getcolor()
        obj = EXTRUDEONE(basis, height, angle_deg, n)
        obj.setcolor(color)
        return obj
    else:
        basis = flatten(basis)
        for obj in basis:
            if obj.dim <> 2: 
                raise ExceptionWT("The base object in EXTRUDE(base, height, angle, n) must be 2-dimensional!") 
        obj = []
        for oo in basis:
            color = oo.getcolor()
            oo3d = EXTRUDEONE(oo, height, angle_deg, n)
            for a in oo3d:
                a.setcolor(color)
            obj.append(oo3d)
        obj = flatten(obj)
        return obj
     
EXT = EXTRUDE
E = EXTRUDE

# ===================================================
# EX
# ===================================================

def EX (args):
	x1 ,x2 = args
	def EX0 (pol):
		dim = PLASM_DIM(pol)
		return PLASM_T(dim+1)(x1)(PLASM_S(dim+1)(x2-x1)(PLASM_EXTRUSION(0.0)(1.0)(pol)))
	return EX0

# ===================================================
# LEX
# ===================================================

def LEX (args):
	x1 , x2 = args
	def LEX0 (pol):
		def SHEARTENSOR (A):
			def SHEARTENSOR0 (POL):
				dim = PLASM_DIM(POL)
				newrow = K((AR([CAT([[0, 1],DIESIS((dim-2))(0)]),A])))
				update = (COMP([CONS, CAT]))([[S1, newrow],AA(SEL)((FROMTO([3,dim+1])))])
				matrix=  update(IDNT(dim+1))              
				return (MAT(matrix))(POL)
			return SHEARTENSOR0

		ret=PLASM_EXTRUSION(0)(1)(pol)
		ret=SHEARTENSOR(x2-x1)(ret)
		ret=S(PLASM_DIM(pol)+1)(x2-x1)(ret)
		ret=PLASM_T(PLASM_DIM(pol)+1)(x1)(ret)
		return ret
	return LEX0

# ===================================================
# SEX 
# ===================================================

def SEX (args):
	x1 , x2 = args
	def SEX1 (height):
		def SEX0 (pol):
			dim = PLASM_DIM(pol)
			ret=PLASM_EXTRUSION(x2-x1)(height)(pol)
			ret=PLASM_S(dim+1)(x2-x1)(ret)
			ret=PLASM_R([dim,dim-1])(x1)(ret)
			return ret
		return SEX0
	return SEX1

if self_test:

	mypol1 = PLASM_T([1, 2, 3])([-5,-5,0])(CUBOID([10,10]))
	mypol2 = PLASM_S(0.9,0.9,0)(mypol1)
	mypol3 =  PLASM_DIFF([mypol1,mypol2]);

	PLASM_VIEW(PLASM_STRUCT([
		  EX([0,10])(mypol3), PLASM_T(1)(12) ,
		  LEX([0,10])(mypol3), PLASM_T(1)(25) ,
		   PLASM_S(3)(3)(SEX([0,PI])(16)(mypol3))
		]))

# ===================================================
# POLAR 
# ===================================================

def POLAR(pol,precision=1e-6):
	faces,cells,pols=UKPOLF(pol)
	for i in range(len(faces)):
		mod=-1*faces[i][0]
		if math.fabs(mod)<precision:mod=1
		faces[i]=[value/mod for value in faces[i][1:]]
	return MKPOL([faces,cells,pols]) 
	
if self_test:
	PLASM_VIEW(POLAR(CUBOID([1,1,1])))

# ===================================================
# SWEEP 
# ===================================================

def SWEEP (v):
    def SWEEP0 (pol):

		ret=Plasm.power(pol, PLASM_QUOTE([1]))

		# shear operation
		mat=IDNT(len(v)+2)
		for i in range(len(v)):
			mat[i+1][len(v)+1]=v[i]
		ret=MAT(mat)(ret)

		return PROJECT(1)(ret)

    return SWEEP0

# ===================================================
# MINKOWSKI
# ===================================================

def MINKOWSKI (vects):
	def MINKOWSKI0 (pol):
		ret=pol
		for i in range(len(vects)-1,-1,-1):
			ret=SWEEP(vects[i])(ret)
		return ret
	return MINKOWSKI0

# ===================================================
# OFFSET 
# ===================================================

def OFFSET (v):
	def OFFSET0 (pol):

		ret=pol
		for i in range(len(v)):

			# shear vector
			shear=[0 if j!=i else v[i] for j in range(len(v))] + [0 for j in range(i)]

			# shear operation
			mat=IDNT(len(shear)+2)
			for i in range(len(shear)):
				mat[i+1][len(shear)+1]=shear[i]
			
			# apply shearing
			ret=MAT(mat)((Plasm.power(ret, PLASM_QUOTE([1]))))

		return PROJECT(len(v))(ret)
	return OFFSET0

if self_test:
	verts = [[0,0,0],[3,0,0],[3,2,0],[0,2,0],[0,0,1.5],[3,0,1.5],[3,2,1.5],[0,2,1.5],[0,1,2.2],[3,1,2.2]]
	cells = [[1,2],[2,3],[3,4],[4,1],[5,6],[6,7],[7,8],[8,5],[1,5],[2,6],[3,7],[4,8],[5,9],[8,9],[6,10],[7,10], [9,10]]
	pols = [[1]]
	House = MKPOL([verts,cells,pols])
	out=Plasm.Struct([ OFFSET([0.1,0.2,0.1])(House), PLASM_T(1)(1.2*PLASM_SIZE(1)(House))(House)])
	PLASM_VIEW(out)


# //////////////////////////////////////////////////////////////////
# THINSOLID
# //////////////////////////////////////////////////////////////////
def THINSOLID (surface,delta=1e-4):

	def map_fn(point):

		u,v,w=point
		# calculate normal as cross product of its gradient
		P0=surface([u,v])
		PX=surface([u+delta,v])
		PY=surface([u,v+delta])
		GX=[PX[i]-P0[i] for i in range(3)]
		GY=[PY[i]-P0[i] for i in range(3)]
		normal=UNITVECT(VECTPROD([GX,GY]))
		ret=[P0[i]+w*normal[i] for i in range(3)]

		return ret

	return map_fn

if self_test:
	Su0 = COMP([PLASM_BEZIERCURVE([[0,0,0],[10,0,0]]),CONS([S1])])
	Su1 = COMP([PLASM_BEZIERCURVE([[0,10,0],[2.5,10,3],[5,10,-3],[7.5,10,3],[10,10,0]]),CONS([S1]) ])
	S0v = COMP([PLASM_BEZIERCURVE([[0,0,0],[0,0,3],[0,10,3],[0,10,0]]) , CONS([S2]) ]) 
	S1v = COMP([PLASM_BEZIERCURVE([[10,0,0],[10,5,3],[10,10,0]]) ,CONS([S2])   ])
	surface=PLASM_COONSPATCH([Su0,Su1,S0v,S1v])
	PLASM_VIEW(PLASM_MAP(  surface ) (Plasm.power(PLASM_INTERVALS(1)(10),PLASM_INTERVALS(1)(10))))
	solidMapping = THINSOLID(surface)
	Domain3D = Plasm.power(Plasm.power(PLASM_INTERVALS(1)(5),PLASM_INTERVALS(1)(5)),PLASM_INTERVALS(0.5)(5))
	PLASM_VIEW(PLASM_MAP(solidMapping)(Domain3D))

	
# //////////////////////////////////////////////////////////////////
# PLANE
# //////////////////////////////////////////////////////////////////

def PLANE (args):

	p0 , p1 , p2 = args
	v1 = VECTDIFF([p1,p0])
	v2 = VECTDIFF([p2,p0])

	side1 = VECTNORM(v1)
	side2 = VECTNORM(v2)

	normal=UNITVECT(VECTPROD([v1,v2]))
	axis=VECTPROD([[0, 0, 1],normal])
	angle = math.acos((INNERPROD([[0, 0, 1],normal])))

	geometry=PLASM_T([1,2,3])(p0)(ROTN([angle, axis])(PLASM_T([1,2])([-1*side1,-1*side2]) (CUBOID([2*side1, 2*side2]))))
	return  [normal, p0, geometry]


# //////////////////////////////////////////////////////////////////
# RATIONAL PLASM_BEZIER
# //////////////////////////////////////////////////////////////////

def RATIONALPLASM_BEZIER (controlpoints_fn):
	degree = len(controlpoints_fn)-1
	basis=BERNSTEINBASIS(S1)(degree)

	def map_fn(point):

		# if control points are functions
		controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

		target_dim=len(controlpoints[0])

		ret=[0 for i in range(target_dim)]
		for i in range(len(basis)):
			coeff=basis[i](point)
			for M in range(target_dim):
				ret[M]+=coeff * controlpoints[i][M] 

		# rationalize (== divide for the last value)
		last=ret[-1]
		if last!=0: ret=[value/last for value in ret]
		ret=ret[:-1]

		return  ret

	return map_fn



# //////////////////////////////////////////////////////////////////
# ELLIPSE
# //////////////////////////////////////////////////////////////////


def ELLIPSE (args):
    Ael, Bel = args
    def ELLIPSE0 (N):
        Cel = 0.5*math.sqrt(2)
        mapping = RATIONALPLASM_BEZIER([[Ael, 0, 1], [Ael*Cel, Bel*Cel, Cel], [0, Bel, 1]])
        quarter = PLASM_MAP(mapping)((PLASM_INTERVALS(1.0)(N)))
        half = PLASM_STRUCT([quarter, PLASM_S(2)(-1)(quarter)])
        return PLASM_STRUCT([half, PLASM_S(1)(-1)(half)])
    return ELLIPSE0

if self_test:
	PLASM_VIEW(ELLIPSE([1,2])(8))

# //////////////////////////////////////////////////////////////////
# NORM2 (==normal of a curve)
# //////////////////////////////////////////////////////////////////

def CURVE_NORMAL(curve):

	def map_fn(point):
		xu,yu=curve(point)
		
		mod2=xu*xu+yu*yu
		den=math.sqrt(mod2) if mod2>0 else 0

		return [-yu/den,xu/den]

	return map_fn

# //////////////////////////////////////////////////////////////////
# DERPLASM_BEZIER
# //////////////////////////////////////////////////////////////////

def DERPLASM_BEZIER (controlpoints_fn):
	degree = len(controlpoints_fn)-1

	# derivative of bernstein
	def DERBERNSTEIN (N):
		def DERBERNSTEIN0 (I):
			def map_fn(point):
				t=S1(point)
				return CHOOSE([N,I]) * math.pow(t,I-1) * math.pow(1-t,N-I-1) * (I-N*t)
			return  map_fn
		return DERBERNSTEIN0


	basis=[DERBERNSTEIN(degree)(i) for i in range(degree+1)]

	def map_fn(point):

		# if control points are functions
		controlpoints=[f(point) if callable(f) else f for f in controlpoints_fn]

		target_dim=len(controlpoints[0])

		ret=[0 for i in range(target_dim)]
		for i in range(len(basis)):
			coeff=basis[i](point)
			for M in range(target_dim):
				ret[M]+=coeff * controlpoints[i][M] 

		return ret

	return map_fn


# //////////////////////////////////////////////////////////////////
# PLASM_BEZIERSTRIPE
# //////////////////////////////////////////////////////////////////

def PLASM_BEZIERSTRIPE (args):
	controlpoints, width, n = args

	bezier  = PLASM_BEZIERCURVE(controlpoints)
	normal  = CURVE_NORMAL(DERPLASM_BEZIER(controlpoints))


	def map_fn(point):

		u,v=point
		bx,by=bezier (point)
		nx,ny=normal (point)
		ret=[bx+v*nx,by+v*ny]

		return ret

	domain=PLASM_S(2)(width)(PLASM_T(1)(0.00001)(Plasm.power(PLASM_INTERVALS(1)(n),PLASM_INTERVALS(1)(1))))
	return PLASM_MAP(map_fn)(domain)

if self_test:
	vertices=[[0,0],[1.5,0],[-1,2],[2,2],[2,0]]
	PLASM_VIEW(Plasm.Struct([ POLYLINE(vertices) , Plasm.power(PLASM_BEZIERSTRIPE([vertices,0.25,22]), PLASM_QUOTE([0.9]))  ]))





# ===================================================
# BSPLINE see http://www.idav.ucdavis.edu/education/CAGDNotes/B-Spline-Curve-Definition.pdf
# ===================================================


def BSPLINE (degree):
	def BSPLINE0 (knots):
		def BSPLINE1 (points_fn):

			n=len(points_fn)-1
			m=len(knots)-1
			k=degree+1
			T=knots
			tmin,tmax=T[k-1],T[n+1]

			# see http://www.na.iac.cnr.it/~bdv/cagd/spline/B-spline/bspline-curve.html
			if len(knots)!=(n+k+1):
				raise Exception("Invalid point/knots/degree for bspline!")

			# de boord coefficients
			def N(i,k,t):

				# Ni1(t)
				if k==1: 
					if (t>=T[i] and t<T[i+1]) or (t==tmax and t>=T[i] and t<=T[i+1]): # i use strict inclusion for the max value
						return 1
					else:
						return 0

				# Nik(t)
				ret=0

				num1,div1= t-T[i], T[i+k-1]-T[i]  
				if div1!=0: ret+=(num1/div1) * N(i,k-1,t)

				num2,div2=T[i+k]-t, T[i+k]-T[i+1]
				if div2!=0:  ret+=(num2/div2) * N(i+1,k-1,t)

				return ret

			# map function
			def map_fn(point):
				t=point[0]

				# if control points are functions
				points=[f(point) if callable(f) else f for f in points_fn]

				target_dim=len(points[0])
				ret=[0 for i in range(target_dim)];
				for i in range(n+1):
					coeff=N(i,k,t) 
					for M in range(target_dim):
						ret[M]+=points[i][M]*coeff
				return ret

			return map_fn

		return BSPLINE1
	return BSPLINE0



# ===================================================
# NUBSPLINE
# ===================================================

def NUBSPLINE(degree,totpoints=80):
	def NUBSPLINE1(knots):
		def NUBSPLINE2(points):
			m=len(knots)
			tmin=min(knots)
			tmax=max(knots)
			tsiz=tmax-tmin
			v=[tsiz/float(totpoints-1) for i in range(totpoints-1)]
			assert len(v)+1==totpoints
			v=[-tmin] + v
			domain = PLASM_QUOTE(v)
			return PLASM_MAP(BSPLINE(degree)(knots)(points))(domain)
		return NUBSPLINE2
	return NUBSPLINE1

# ===================================================
# DISPLAYNUBSPLINE
# ===================================================

def DISPLAYNUBSPLINE (args,marker_size=0.1):
	degree, knots, points = args

	spline_view_knots=POLYMARKER(2,marker_size)(UKPOL(NUBSPLINE(degree,len(knots))(knots)(points))[0])

	return  PLASM_STRUCT([
		NUBSPLINE(degree)(knots)(points) if degree>0 else POLYMARKER(3,marker_size)(points)
		,spline_view_knots
		,POLYLINE(points)
		,POLYMARKER(1,marker_size)(points)
	])


if self_test:
	ControlPoints=[[0,0],[-1,2],[1,4],[2,3],[1,1],[1,2],[2.5,1], [2.5,3], [4,4],[5,0]]
	PLASM_VIEW(DISPLAYNUBSPLINE([3,[0,0,0,0, 1,2,3,4,5, 6    ,7,7,7,7], ControlPoints]))


# =================================================
# RATIONALBSPLINE
# =================================================    


def RATIONALBSPLINE (degree):
	def RATIONALBSPLINE0 (knots):
		def RATIONALBSPLINE1 (points):

			bspline=BSPLINE(degree)(knots)(points)

			def map_fn(point):			

				ret=bspline(point)

				# rationalize (== divide for the last value)
				last=ret[-1]
				if last!=0: ret=[value/last for value in ret]
				ret=ret[:-1]
				return ret

			return map_fn

		return RATIONALBSPLINE1
	return RATIONALBSPLINE0


# =================================================
# NURBSPLINE
# =================================================

def NURBSPLINE(degree,totpoints=80):
	def NURBSPLINE1(knots):
		def NURBSPLINE2(points):
			m=len(knots)
			tmin=min(knots)
			tmax=max(knots)
			tsiz=tmax-tmin
			v=[tsiz/float(totpoints-1) for i in range(totpoints-1)]
			assert len(v)+1==totpoints
			v=[-tmin] + v
			domain = PLASM_QUOTE(v)
			return PLASM_MAP(RATIONALBSPLINE(degree)(knots)(points))(domain)
		return NURBSPLINE2
	return NURBSPLINE1


# ===================================================
# DISPLAYNURBSPLINE
# ===================================================


def DISPLAYNURBSPLINE (args,marker_size=0.1):
	degree, knots, points = args

	spline_view_knots=POLYMARKER(2,marker_size)(UKPOL(NURBSPLINE(degree,len(knots))(knots)(points))[0])

	return  PLASM_STRUCT([
		NURBSPLINE(degree)(knots)(points) if degree>0 else POLYMARKER(3,marker_size)(points)
		,spline_view_knots
		,POLYLINE(points)
		,POLYMARKER(1,marker_size)(points)
	])


if self_test:
	knots = [0,0,0,1,1,2,2,3,3,4,4,4]
	_p=math.sqrt(2)/2.0
	controlpoints = [[-1,0,1], [-_p,_p,_p], [0,1,1], [_p,_p,_p],[1,0,1], [_p,-_p,_p], [0,-1,1], [-_p,-_p,_p], [-1,0,1]]
	PLASM_VIEW(DISPLAYNURBSPLINE([2, knots, controlpoints]))



#===================================================================================
# Colors (wants a list [R,G,B] or [R,G,B,A]
# Example PLASM_COLOR([1,0,0])(pol)
#===================================================================================

# Change it to procedural style:
# English:
def COLOR(obj, col):
  # obj may be a single object or a list of objects
  if not isinstance(obj, list):
    obj.setcolor(col)
  else:
    obj = flatten(obj)
    for x in obj: x.setcolor(col)
  return COPY(obj)

C = COLOR
# Czech:
BARVA = COLOR
OBARVI = COLOR
OBARVIT = COLOR
# Polish:
KOLOR = COLOR
# German:
FARBE = COLOR
# Spanish:
# Same as in English
# Italian:
COLORE = COLOR
# French:
COULEUR = COLOR

# Original PLaSM color command:
def PLASM_COLOR(Cpl):
	def formatColor(Cpl):
		assert isinstance(Cpl, Color4f) 
		return "%s %s %s %s" % (Cpl.r,Cpl.g,Cpl.b,Cpl.a)

	# convert list to Color
	if isinstance(Cpl, list) and len(Cpl) in (3, 4):
                # Normalizing RGB between 0 and 1 if necessary:
                if Cpl[0] > 1 or Cpl[1] > 1 or Cpl[2] > 1:
		    Cpl[0] = Cpl[0] / 255.
		    Cpl[1] = Cpl[1] / 255.
		    Cpl[2] = Cpl[2] / 255.
		Cpl=Color4f(Cpl[0],Cpl[1],Cpl[2],Cpl[3] if len(Cpl)>=4 else 1.0)
        else: ExceptionWT("Invalid color!")

	def PLASM_COLOR0(pol):
		return Plasm.addProperty(pol, "RGBcolor", formatColor(Cpl))

	return PLASM_COLOR0
# English:
GRAY    = [128, 128, 128]
GREY    = [128, 128, 128]

LIGHTGREEN   = [0, 255, 0]
GREEN   = [0, 180, 0]
DARKGREEN   = [0, 100, 0]

BLACK   = [0, 0, 0]

LIGHTBLUE    = [0, 0, 255]
BLUE    = [0, 0, 180]
DARKBLUE    = [0, 0, 100]

LIGHTBROWN   = [204, 102, 0]
BROWN   = [153, 76, 0]
DARKBROWN   = [102, 51, 0]

LIME = [0,255,0]
MAROON = [128,0,0]
OLIVE = [128,128,0]
TEAL = [0,128,128]
NAVY = [0,0,128]
NAVYBLUE = [0,0,128]
CRIMSON = [220,20,60]
CORAL = [255,127,80]
SALMON = [250,128,114]
KHAKI = [240,230,140]
TURQUOISE = [64,224,208]
ORCHID = [218,112,214]
BEIGE = [245,245,220]
WHEAT = [245,222,179]

LIGHTCYAN    = [0, 255, 255]
CYAN    = [0, 180, 180]
DARKCYAN    = [0, 100, 100]

PINK =    [255, 0, 255]

LIGHTMAGENTA = [255, 0, 255]
MAGENTA = [180, 0, 180]
DARKMAGENTA = [100, 0, 100]

LIGHTORANGE  = [255, 153, 0]
ORANGE  = [180, 107, 0]
DARKORANGE  = [100, 60, 0]

PURPLE  = [128, 0, 128]

INDIGO =  [75, 0, 130]

VIOLET =  [238, 130, 238]

WHITE   = [255, 255, 255]

LIGHTRED     = [255, 0, 0]
RED     = [180, 0, 0]
DARKRED     = [100, 0, 0]

LIGHTYELLOW  = [255, 255, 0]
YELLOW  = [180, 180, 0]
DARKYELLOW  = [100, 100, 0]

STEEL =   [200, 200, 200]
BRASS =   [255, 250, 83]
COPPER =  [184, 115, 51]
BRONZE =  [140, 120, 83]
SILVER =  [230, 232, 250]
GOLD =    [226, 178, 39]

# Czech:
SEDA = GRAY
SEDIVA = GRAY
ZELENA = GREEN
CERNA = BLACK
MODRA = BLUE
HNEDA = BROWN
ORANZOVA = ORANGE
RUZOVA = PINK
FIALOVA = PURPLE
BILA = WHITE
CERVENA = RED
RUDA = RED
ZLUTA = YELLOW
OCEL = STEEL
OCELOVA = STEEL
MOSAZ = BRASS
MOSAZNA = BRASS
MED = COPPER
MEDENA = COPPER
BRONZ = BRONZE
BRONZOVA = BRONZE
STRIBRO = SILVER
STRIBRNA = SILVER
ZLATO = GOLD
ZLATA = GOLD
# Polish:
SZARY = GRAY
SIWY = GRAY
ZIELONY = GREEN
CZARNY = BLACK
NIEBIESKI = BLUE
BRAZOWY = BROWN
POMARANCZOVY = ORANGE
ROZOWY = PINK
PURPUROWY = PURPLE
BIALY = WHITE
CZERWONY = RED
ZOLTY = YELLOW
STAL = STEEL
STALOWY = STEEL
MOSIADZ = BRASS
MIEDZ = COPPER
BRAZ = BRONZE
BRAZOWY = BRONZE
SREBRO = SILVER
SREBRNY = SILVER
ZLOTO = GOLD
ZLOTY = GOLD
# German:
GRAU = GREY
GRUEN = GREEN
GRUN = GREEN
SCHWARZ = BLACK
BLAU = BLUE
BRAUN = BROWN
    # ORANGE is the same
ROSA = PINK
LILA = PURPLE
WEISS = WHITE
ROT = RED
GELB = YELLOW
STAHL = STEEL
MESSING = BRASS
KUPFER = COPPER
    # BRONZE is the same
SILBER = SILVER
    # GOLD is the same
# Spanish:
GRIS = GREY
VERDE = GREEN
NEGRO = BLACK
NEGRA = BLACK
AZUL = BLUE
MARRON = BROWN
CIAN = CYAN
ROSO = PINK
ROSA = PINK
MAGENTA = MAGENTA
NARANJA = ORANGE
PURPURO = PURPLE
PURPURA = PURPLE
BLANCO = WHITE
BLANCA = WHITE
ROJO = RED
ROJA = RED
AMARILLO = YELLOW
AMARILLA = YELLOW
ACERO = STEEL
LATON = BRASS
COBRE = COPPER
BRONCE = BRONZE
PLATA = SILVER
ORO = GOLD
# Italian:
GRIGIO = GREY
VERDE = GREEN
NERO = BLACK
NERA = BLACK
AZZURRO = BLUE
AZZURRA = BLUE
MARRONE = BROWN
ROSOLARE = BROWN
CIANO = CYAN
DENTELLARE = PINK
ROSA = PINK
MAGENTA = MAGENTA
ARANCIONE = ORANGE
ARANCIO = ORANGE
ARANCIA = ORANGE
VIOLA = PURPLE
VIOLA = PURPLE
PORPORA = PURPLE
BIANCO = WHITE
BIANCA = WHITE
ROSSO = RED
ROSSA = RED
GIALLO = YELLOW
GIALLA = YELLOW
ACCIAIO = STEEL
OTTONE = BRASS
RAME = COPPER
BRONZO = BRONZE
ARGENTO = SILVER
# ORO is same as in Spanish
# French:
GRIS = GREY
VERT = GREEN
NOIR = BLACK
BLEU = BLUE
BRUN = BROWN
# CYAN is same as in English
ROSE = PINK
# MAGENTA same as in English
# ORANGE same as in English
POURPRE = PURPLE
BLANC = WHITE
ROUGE = RED
JAUNE = YELLOW
ACIER = STEEL
LAITON = BRASS
CUIVRE = COPPER
# BRONZE same as in English
ARGENT = SILVER
OR = GOLD


# Returns a list of three numbers between 0 and 255: [R, G, B]
# A and other properties not taken into account yet.
def PLASM_GETCOLOR(obj):
   if not ISPOL(obj):
      raise Exception(repr(obj) + " is not a Plasm object!")
   string = Plasm.getProperty(obj, "RGBcolor")
   col = [float(s) for s in string.split()] 
   if col == []:
      return col
   else:
      if len(col) < 3:
          print "Warning: There is some problem with the color of an object."
          print "Expected [R, G, B] but list length is", len(col0)
          return
   col[0] = int(255*float(col[0]) + 0.5)
   col[1] = int(255*float(col[1]) + 0.5)
   col[2] = int(255*float(col[2]) + 0.5)
   return col[0:3]
 

if self_test: 
   (Plasm.getProperty(PLASM_COLOR(RED)(Plasm.cube(3)),"RGBcolor")==("%s %s %s %s" % (1.0,0.0,0.0,1.0)))


#===================================================================================
# Materials (want a list of 17 elements(ambientRGBA, diffuseRGBA specularRGBA emissionRGBA shininess)
# Example PLASM_MATERIAL([1,0,0,1,  0,1,0,1,  0,0,1,0, 0,0,0,1, 100])(pol)
#===================================================================================

def PLASM_MATERIAL(M):

	def PLASM_MATERIAL0(pol):

		svalue="%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (M[ 0],M[ 1],M[ 2],M[ 3],M[ 4],M[ 5],M[ 6],M[ 7],M[ 8],M[ 9],M[10],M[11],M[12],M[13],M[14],M[15],M[16])
		return Plasm.addProperty(pol, "VRMLmaterial", svalue) 

	# convert list to Material
	if isinstance(M,list) and (len(M)==3 or len(M)==4):
		r,g,b=M[0:3]
		alpha=M[3] if len(M)==4 else 1.0
		ambient =[r*0.4,g*0.4,b*0.4,alpha]
		diffuse =[r*0.6,g*0.6,b*0.6,alpha]
		specular=[0    ,0    ,0    ,alpha]
		emission=[0    ,0    ,0    ,alpha]
		shininess = 1.0
		M=ambient + diffuse + specular + emission + [shininess]

	#convert the list to a XGE material
	if not (isinstance(M,list) and len(M)==17):
		raise Exception("cannot transform " + repr(M) + " in a material (which is a list of 17 floats, ambient,diffuse,specular,emission,shininess)!")

	return PLASM_MATERIAL0

if self_test:
   (Plasm.getProperty(PLASM_MATERIAL([1,0,0,1,  0,1,0,1,  0,0,0,1,  0,0,0,1,  100])(Plasm.cube(3)),"VRMLmaterial")==[1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,100])

# New definition:
def MATERIAL(obj, mat):
  # obj may be a single object or a list of objects
  if not isinstance(obj, list):
    obj.setmaterial(mat)
  else:
    obj = flatten(obj)
    for x in obj: x.setmaterial(mat)
  return COPY(obj)

#===================================================================================
# Textures (wants a list [url:string,repeatS:bool,repeatT:bool,cx::float,cy::float,rot::float,sx::float,sy::float,tx::float,ty::float]
# Example TEXTURE('filename.png')(pol)
#===================================================================================

def TEXTURE(params):

	def TEXTURE0(params,pol):

		# is simply an URL
		if isinstance(params,str):
			url=params
			params=[]
		# is a list with a configuration
		else:
			assert isinstance(params,list) and len(params)>=1
			url=params[0]
			if not isinstance(url,str): 
				raise Exception("Texture error " + repr(url) + " is not a path!")
			params=params[1:]

		# complete with default parameters
		params+=[True,True, 0.0,0.0,  0.0,   1.0,1.0,    0.0,0.0   ][len(params):]

		# unpack
		repeatS, repeatT, cx, cy, rot, sx, sy, tx, ty=params

		spacedim = Plasm.getSpaceDim(pol)
		
		if not (spacedim in (2,3)):
			# raise Exception("Texture cannot be applyed only to 2 or 3 dim pols!")
			return Plasm.copy(pol)

		box = Plasm.limits(pol)
		ref0,ref1=[box.maxsizeidx(),box.minsizeidx()]

		if (spacedim==3):
			ref1=1 if (ref0!=1 and ref1!=1) else (2 if (ref0!=2 and ref1!=2) else 3)
			
		assert ref0!=ref1
		
		# empty box
		if (box.size()[ref0]==0 or box.size()[ref1]==0):
			return Plasm.copy(pol)
		
		# translate vector
		vt=Vecf(0.0, \
			-box.p1[1] if box.dim()>=1 else 0.0, \
			-box.p1[2] if box.dim()>=2 else 0.0, \
			-box.p1[3] if box.dim()>=3 else 0.0)
		
		# scale vector
		vs=Vecf(0.0, \
			1.0/(box.size()[1]) if box.dim()>=1 and box.size()[1] else 1.0, \
			1.0/(box.size()[2]) if box.dim()>=2 and box.size()[2] else 1.0, \
			1.0/(box.size()[3]) if box.dim()>=3 and box.size()[3] else 1.0)
		
		# permutation
		refm=1 if (ref0!=1 and ref1!=1) else (2 if (ref0!=2 and ref1!=2) else 3)
		assert ref0!=ref1 and ref1!=refm and ref0!=refm
		perm=[0,0,0,0]
		perm[ref0]=1
		perm[ref1]=2
		perm[refm]=3 


		project_uv=Matf.translateV (Vecf(0.0,+cx,+cy,0)) \
				* Matf.scaleV (Vecf(0.0,sx,sy,1)) \
				* Matf.rotateV(3,1,2,-rot) \
				* Matf.translateV (Vecf(0.0,-cx,-cy,0)) \
				* Matf.translateV (Vecf(0.0,tx,ty,0))  \
				* Matf(3).swapCols(perm) \
				* Matf.scaleV     (vs) \
				* Matf.translateV (vt)


		return Plasm.Skin(pol,url,project_uv)

	return lambda pol: TEXTURE0(params,pol)

if self_test:
	PLASM_VIEW(TEXTURE(":images/gioconda.png")(CUBOID([1,1])))



# //////////////////////////////////////////////////////////////
def BOUNDARY(hpc,dim):

	"""
		Find all boundary faces of dimension <cell_dim> inside an hpc,
		Extract only faces from FULL hpc, skipping "embedded" hpc 
	"""

	# here i will store the return value, ie all the boundary cells
	vertex_db=[]
	faces_db =[]

	def getCells(g,dim):
		""" local utility: get all cells of a certain dimension inside an hasse diagram """
		ret=[]
		it=g.each(dim)
		while not it.end():
			ret.append(it.getNode())
			it.goForward()
		return ret

	def getVerticesId(g,cell):

		""" local utility: return all vertices id of a generic cell inside an hasse diagram """

		# special navigator to find cells inside an hasse diagram
		nav=GraphNavigator()

		# extract all vertices if from this face
		nv=g.findCells(0, cell,nav)
	
		return [nav.getCell(0,I) for I in range(nv)]


	# flat the hpc to two levels
	temp=Plasm.shrink(hpc,False)

	for node in temp.childs:

		# this is the hasse diagram
		g=node.g

		# no geometry in the node, useless hpc node
		if g is None: continue

		# check if the hpc is  "full", and not "embedded"
		if node.spacedim!=node.pointdim or node.pointdim!=g.getPointDim(): 
			continue

		# this hpc is in different dimension
		if (dim+1)!=node.pointdim: 
			continue

		# this is the transformation matrix inside the child hpc
		T=node.vmat

		# iterate in all <dim>-cells
		for face in getCells(g,dim):

			# it's an internal face
			if g.getNUp(face)==2: continue 

			new_face=[]

			# this is the new boundary face	
			for Id in getVerticesId(g,face):

				# get the geometry as a Vecf and transform using T
				vertex =T * g.getVecf(Id)

				# convert the Vecf to a python list	(removing the homo components)		
				vertex=[vertex[i]/vertex[0] for i in range(1,dim+2)]

				if not vertex in vertex_db:
					vertex_db.append(vertex)

				new_face.append(vertex_db.index(vertex))

			# consider it as the unordered list of vertex indices, I sort it
			faces_db.append(sorted(new_face))
				
	return [vertex_db,faces_db]

#print "...fenvs.py imported in",(time.clock() - start),"seconds"


#===================================================================================
# AUTOGRADING FUNCTIONALITY
#===================================================================================

# Base function. Returns True if object "tested" contains 
# the entire object "obj":
def HASOBJECT(tested, obj, tol = 1e-8):
    objint = INTERSECTION(tested, obj)
    test = DIFF(obj, objint)
    s1 = test.sizex()
    s2 = test.sizey()
    s3 = 0
    if test.getdimension() == 3:
      s3 = test.sizez()
    if s1 < tol and s2 < tol and s3 < tol:
      return True
    else:
      return False

# Base function. Returns True if object "tested" contains 
# no part of object "obj":
def HASNTOBJECT(tested, obj, tol = 1e-8):
    test = INTERSECTION(tested, obj)
    s1 = test.sizex()
    s2 = test.sizey()
    s3 = 0
    if test.getdimension() == 3:
      s3 = test.sizez()
    if s1 < tol and s2 < tol and s3 < tol:
      return True
    else:
      return False

# Returns True if the entire square "square" lies in object "tested":
def HASSQUARE(tested, centerx, centery, size):
    square = SQUARE(size)
    MOVE(square, centerx - 0.5*size, centery - 0.5*size)
    return HASOBJECT(tested, square)

# Returns True if no part of square "square" lies in object "tested":
def HASNTSQUARE(tested, centerx, centery, size):
    square = SQUARE(size)
    MOVE(square, centerx - 0.5*size, centery - 0.5*size)
    return HASNTOBJECT(tested, square)

# Returns True if the entire cube "cube" lies in object "tested":
def HASCUBE(tested, centerx, centery, centerz, size):
    cube = CUBE(size)
    MOVE(cube, centerx - 0.5*size, centery - 0.5*size, centerz - 0.5*size)
    return HASOBJECT(tested, cube)

# Returns True if no part of cube "cube" lies in object "tested":
def HASNTCUBE(tested, centerx, centery, centerz, size):
    cube = CUBE(size)
    MOVE(cube, centerx - 0.5*size, centery - 0.5*size, centerz - 0.5*size)
    return HASNTOBJECT(tested, cube)

# Returns True if entire rectangle "rect" lies in object "tested":
def HASRECTANGLE(tested, centerx, centery, sizex, sizey):
    rect = RECTANGLE(sizex, sizey)
    MOVE(rect, centerx - 0.5*sizex, centery - 0.5*sizey)
    return HASOBJECT(tested, rect)

# Returns True if no part of rectangle "rect" lies in object "tested":
def HASNTRECTANGLE(tested, centerx, centery, sizex, sizey):
    rect = RECTANGLE(sizex, sizey)
    MOVE(rect, centerx - 0.5*sizex, centery - 0.5*sizey)
    return HASNTOBJECT(tested, rect)

# Returns True if entire brick "brick" lies in object "tested":
def HASBRICK(tested, centerx, centery, centerz, sizex, sizey, sizez):
    brick = BRICK(sizex, sizey, sizez)
    MOVE(brick, centerx - 0.5*sizex, centery - 0.5*sizey, centerz - 0.5*sizez)
    return HASOBJECT(tested, brick)

# Returns True if no part of brick "brick" lies in object "tested":
def HASNTBRICK(tested, centerx, centery, centerz, sizex, sizey, sizez):
    brick = BRICK(sizex, sizey, sizez)
    MOVE(brick, centerx - 0.5*sizex, centery - 0.5*sizey, centerz - 0.5*sizez)
    return HASNTOBJECT(tested, brick)

# Checks if 2D object "tested" has dimensions sizex, sizey
# with a given tolerance:
def SIZETEST2D(tested, sizex, sizey, eps = 0.0):
    a1 = (tested.sizex() - sizex <= eps)
    a2 = (tested.sizey() - sizey <= eps)
    return (a1 and a2)

# Checks if 3D object "tested" has dimensions sizex, sizey, sizez
# with a given tolerance:
def SIZETEST3D(tested, sizex, sizey, sizez, eps = 0.0):
    a1 = (tested.sizex() - sizex <= eps)
    a2 = (tested.sizey() - sizey <= eps)
    a3 = (tested.sizez() - sizez <= eps)
    return (a1 and a2 and a3)

# Checks if 2D objects "tested" and "ref" have the same dimensions, 
# with a given tolerance:
def SIZEMATCH2D(tested, ref, eps = 0.0):
    a1 = (tested.sizex() - ref.sizex() <= eps)
    a2 = (tested.sizey() - ref.sizey() <= eps)
    return (a1 and a2)

# Checks if 3D objects "tested" and "ref" have the same dimensions, 
# with a given tolerance:
def SIZEMATCH3D(tested, ref, eps = 0.0):
    a1 = (tested.sizex() - ref.sizex() <= eps)
    a2 = (tested.sizey() - ref.sizey() <= eps)
    a3 = (tested.sizez() - ref.sizez() <= eps)
    return (a1 and a2 and a3)

# Checks if 2D object "tested" has given minx, miny 
# coordinates in the x, y directions, with a given tolerance:
def POSITIONTEST2D(tested, minx, miny, eps = 0.0):
    b1 = (abs(tested.minx() - minx) <= eps)
    b2 = (abs(tested.miny() - miny) <= eps)
    return (b1 and b2)

# Checks if 3D object "tested" has given minx, miny, minz 
# coordinates in the x, y, z directions, with a given tolerance:
def POSITIONTEST3D(tested, minx, miny, minz, eps = 0.0):
    b1 = (abs(tested.minx() - minx) <= eps)
    b2 = (abs(tested.miny() - miny) <= eps)
    b3 = (abs(tested.minz() - minz) <= eps)
    return (b1 and b2 and b3)

# Checks if 2D objects "tested" and "ref" have the same 
# minimum coordinates in the x, y directions, 
# with a given tolerance:
def POSITIONMATCH2D(tested, ref, eps = 0.0):
    b1 = (abs(tested.minx() - ref.minx()) <= eps)
    b2 = (abs(tested.miny() - ref.miny()) <= eps)
    return (b1 and b2)

# Checks if 3D objects "tested" and "ref" have the same 
# minimum coordinates in the x, y, z directions, 
# with a given tolerance:
def POSITIONMATCH3D(tested, ref, eps = 0.0):
    b1 = (abs(tested.minx() - ref.minx()) <= eps)
    b2 = (abs(tested.miny() - ref.miny()) <= eps)
    b3 = (abs(tested.minz() - ref.minz()) <= eps)
    return (b1 and b2 and b3)

# Move 2D object "tested" so that it has given minx, miny:
def ADJUSTPOSITION3D(tested, minx, miny):
    xmintested = tested.minx()
    ymintested = tested.miny()
    return MOVE(tested, minx - xmintested, miny - ymintested)

# Move 3D object "tested" so that it has given minx, miny, minz:
def ADJUSTPOSITION3D(tested, minx, miny, minz):
    xmintested = tested.minx()
    ymintested = tested.miny()
    zmintested = tested.minz()
    return T(tested, minx - xmintested, miny - ymintested, minz - zmintested)

# Move 2D object "tested" so that its minx coincides with minx of object ref,
# and its miny coincides with miny of object ref:
def ALIGNOBJECTS2D(tested, ref):
    xmintested = tested.minx()
    ymintested = tested.miny()
    xminref = ref.minx()
    yminref = ref.miny()
    return MOVE(tested, xminref - xmintested, yminref - ymintested)

# Move 3D object "tested" so that its minx coincides with minx of object ref,
# its miny coincides with miny of object ref. and its minz coincides 
# with minz of object ref:
def ALIGNOBJECTS3D(tested, ref):
    xmintested = tested.minx()
    ymintested = tested.miny()
    zmintested = tested.minz()
    xminref = ref.minx()
    yminref = ref.miny()
    zminref = ref.minz()
    return MOVE(tested, xminref - xmintested, yminref - ymintested, zminref - zmintested)

# Returns a rectangle which is the bounding box of a 2D object "tested":
def BBOX2D(tested):
    rect = RECTANGLE(tested.maxx() - tested.minx(), tested.maxy() - tested.miny())
    MOVE(rect, tested.minx(), tested.miny())
    return rect

# Returns a brick which is the bounding box of a 3D object "tested":
def BBOX3D(tested):
    brick = BOX(tested.maxx() - tested.minx(), tested.maxy() - tested.miny(), tested.maxz() - tested.minz())
    MOVE(brick, tested.minx(), tested.miny(), tested.minz())
    return brick

# Returns the frame of a 2D bounding box "bbox". Bars of 
# the frame will have thickness "eps"
def BBOXFRAME2D(bbox, eps):
    x = bbox.sizex()
    y = bbox.sizey()
    rect = RECTANGLE(x - 2*eps, y - 2*eps)
    MOVE(rect, eps, eps)
    return DIFF(bbox, rect)

# Returns the frame of a 3D bounding box "bbox". Bars of 
# the frame will have thickness "eps"
def BBOXFRAME3D(bbox, eps):
    x = bbox.sizex()
    y = bbox.sizey()
    z = bbox.sizez()
    brickx = BOX(x, y - 2*eps, z - 2*eps)
    T(brickx, 0, eps, eps)
    bricky = BOX(x - 2*eps, y, z - 2*eps)
    T(bricky, eps, 0, eps)
    brickz = BOX(x - 2*eps, y - 2*eps, z)
    T(brickz, eps, eps, 0)
    return DIFF(bbox, brickx, bricky, brickz)

# Alberto's changes to make Cartesian products simplicial:
def cumsum(iterable):
    """ Cumulative addition: list(cumsum(range(4))) => [0, 1, 3, 6] 
        
        Return a list of numbers
    """
    iterable = iter(iterable)
    s = iterable.next()
    yield s
    for c in iterable:
        s = s + c
        yield s

def larExtrude(model,pattern):
    """ Multidimensional extrusion 
        model is a LAR model: a pair (vertices, cells)
        pattern is a list of positive and negative sizes (multi-extrusion)
        
        Return a "model"
    """
    V, FV = model
    d, m = len(FV[0]), len(pattern)
    coords = list(cumsum([0]+(AA(ABS)(pattern))))
    offset, outcells, rangelimit = len(V), [], d*m
    for cell in FV:
        tube = [v + k*offset for k in range(m+1) for v in cell]
        cellTube = [tube[k:k+d+1] for k in range(rangelimit)]
        outcells += [reshape(cellTube, newshape=(m,d,d+1)).tolist()]
    
    outcells = AA(CAT)(TRANS(outcells))
    cellGroups = [group for k,group in enumerate(outcells) if pattern[k]>0 ]
    outVertices = [v+[z] for z in coords for v in V]
    outModel = outVertices, CAT(cellGroups)
    return outModel

def larSimplexGrid(shape):
    """ User interface in LARCC.
        
        Return an (hyper-)cuboid of given shape. Vertices have integer coords
    """
    model = V0,CV0 = [[]],[[0]]    # the empty simplicial model
    for item in shape:
        model = larExtrude(model,item * [1])
    return model

def SIMPLEXGRID(size):
    """ User interface in Pyplasm.
        size = list of grid sizes in each coordinate direction;
        shape = list of numbers of steps in each coordinate direction.
        
        SIMPLEXGRID(size)(shape): Return an HPC value
    """
    def model2hpc0(shape):
        assert len(shape) == len(size)
        scaleCoeffs = map(DIV, zip(size,shape))
        model = larSimplexGrid(shape)
        verts,cells = model
        cells = [[v+1 for v in cell] for cell in cells]
        coords = range(1,len(size)+1)
        return PLASM_S(coords)(scaleCoeffs)(MKPOL([verts,cells,None]))
    return model2hpc0

# NEW COMMAND FOR REFERENCE DOMAIN:

def REF_DOMAIN(a, b, m, n):
    #return POWER(INTERVALS(a, m), INTERVALS(b, n))
    return SIMPLEXGRID([a, b])([m, n])

def UNIT_SQUARE(n, m):
    #return POWER(INTERVALS(1.0, n), INTERVALS(1.0, m))
    return SIMPLEXGRID([1.0, 1.0])([m, n])
