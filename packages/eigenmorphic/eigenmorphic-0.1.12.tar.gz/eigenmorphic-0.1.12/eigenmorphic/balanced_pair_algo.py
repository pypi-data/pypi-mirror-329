from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ
from sage.combinat.words.word import Word
from sage.matrix.special import identity_matrix
from sage.matrix.constructor import matrix
from sage.modules.free_module_element import vector
from eigenmorphic.eigenvalues import dimension_eigenvalues, morphic_eigenvalues
from eigenmorphic.coboundary import coboundary_basis
from sage.rings.number_field.number_field import NumberField
from sage.modules.free_module import VectorSpace
from sage.arith.functions import lcm

def return_words(s, w=None, verb=0):
    """
    Find return words on w for sustitution s,
    where w is a prefix of a fixed point of s.
    If w is None, take first letter of a fixed point.

    A word u is a return word for w if
    - uw is in the language of s,
    - w is a prefix of u, and there is no other occurence of w in u

    INPUT:
        - ``s`` - WordMorphism - the substitution
        - ``w`` - Word (default: ``None``) - a prefix of a fixed point of s
        - ``verb`` - int (default: 0) - If > 0, print informations

    OUTPUT:
        A set of return words.

    EXAMPLES::
        sage: from eigenmorphic import *
        sage: s = WordMorphism('1->112,2->2321,3->12')
        sage: return_words(s, '1')
        {word: 1, word: 12, word: 12232, word: 1232}
    """
    if w is None:
        w = s.fixed_points()[0][:1]
        if verb > 0:
            print("w = " + str(w))
    else:
        w = Word(w, alphabet=s.domain().alphabet())
    to_see = set([w])
    res = set(to_see)
    while len(to_see) > 0:
        to_see2 = set()
        for r in to_see:
            r2 = s(r)
            ri = 0
            for i in range(1,len(r2)-len(w)+1):
                if r2[i:i+len(w)] == w:
                    r3 = r2[ri:i]
                    if r3 not in res:
                        res.add(r3)
                        to_see2.add(r3)
                    ri = i
            r3 = r2[ri:]
            if r3 not in res:
                res.add(r3)
                to_see2.add(r3)
        to_see = to_see2
    return res

def is_balanced(u,v, pv=None):
    """
    Test if a couple of words is balanced for projection pv.

    INPUT:
        - ``u`` - Word
        - ``v`` - Word
        - ``pv`` - (default: ``None``) - vector or matrix - projection

    OUPTUT:
        A bool.

    EXAMPLES::
        sage: from eigenmorphic.balanced_pair_algo import is_balanced
        sage: w = Word('1221', alphabet=list('123'))
        sage: is_balanced(w[:2], w[2:], vector((1,1,1)))
        True
        sage: is_balanced(w[:2], w[2:])
        True
    """
    if pv is None:
        pv = identity_matrix(u.parent().alphabet().cardinality())
    return pv*(vector(u.abelian_vector()) - vector(v.abelian_vector())) == 0

def is_prefix(w, s):
    """
    Determine if w is a prefix of a fixed point of s.
    Assume that w[:1] is a prefix of a fixed point of s.
    """
    return w.is_prefix(s.fixed_point(w[:1][0]))

def decompose(u, v, pv=None):
    """
    Decompose a balanced pair into irreducible pairs, for a projection pv.

    INPUT:
        - ``u`` - Word
        - ``v`` - Word
        - ``pv`` - (default: ``None``) - vector or matrix - projection

    OUTPUT:
        List of irreducible balanced pairs (list of couples of words)

    EXAMPLES::
        sage: from eigenmorphic.balanced_pair_algo import decompose
        sage: s = WordMorphism('a->ab,b->ac,c->a')
        sage: decompose(s('ab'), s('ba'))
        [(word: a, word: a), (word: bac, word: cab)]
    """
    if pv is None:
        pv = identity_matrix(u.parent().alphabet().cardinality())
    r = []
    ri = 0
    for i in range(1,len(u)+1):
        u1, v1 = u[ri:i], v[ri:i]
        if is_balanced(u1, v1, pv):
            r.append((u1, v1))
            ri = i
    return r

def first_balanced_pairs(s, w, pv, verb=0):
    """
    First set of balanced pairs in the balanced pair algorithm.

    INPUT:
        - ``s`` - WordMorphism - the substitution, assumed to have a fixed point
        - ``w`` - Word - prefix of a fixed point of s
        - ``pv`` - (default: ``None``) - vector or matrix - projection
        - ``verb`` - int (default: 0) - If > 0, print informations

    OUTPUT:
        A set of balanced pairs (couples of words).

    EXAMPLES::
        sage: from eigenmorphic.balanced_pair_algo import first_balanced_pairs
        sage: s = WordMorphism('1->112,2->2321,3->12')
        sage: first_balanced_pairs(s, Word('1', alphabet=list('123')), identity_matrix(3))
        {(word: 1, word: 1),
         (word: 12, word: 21),
         (word: 12232, word: 22321),
         (word: 1232, word: 2321)}
    """
    lr = return_words(s, w, verb-1)
    lb = [(u, u[len(w):]+w) for u in lr]
    lb2 = set()
    for u,v in lb:
        lb2.update(decompose(u, v, pv))
    return lb2

def balanced_pair_algorithm(s, w=None, pv=None, getgraph=0, getbp=0, verb=0, stop_event=None):
    """
    Balanced pair algorithm, to test if the subshift of s has pure discrete spectrum,
    from "A generalized balanced pair algorithm" by Brian F. Martensen

    INPUT:
        - ``s`` - WordMorphism -- the substitution
        - ``w`` - Word -- prefix of a periodic point of s
        - ``pv`` - (default: ``None``) - vector or matrix - projection
        - ``getgraph`` - bool (default: ``False``) -- if True, return balanced pairs and the graph on balanced pairs, represented with entering edges
        - ``getbp`` - bool (default: ``False``) -- if True, return the set of balanced pairs stable by the susbtitution
        - ``verb`` - int (default: 0) - If > 0, print informations
        - ``stop_event`` - multiprocessing.Event (default: ``None``) -- used to stop the function

    OUTPUT:
        A bool.

    EXAMPLES::
        sage: from eigenmorphic import *
        sage: s = WordMorphism('a->ab,b->ac,c->a')
        sage: balanced_pair_algorithm(s)
        True
        sage: s = WordMorphism('a->Ab,b->A,A->aB,B->a')
        sage: balanced_pair_algorithm(s)
        False
        sage: s = WordMorphism('1->31,2->412,3->312,4->412')
        sage: balanced_pair_algorithm(s)
        True

        # Example giving wrong answer
        # because the prefix w does not satisfy the condition that w+w[:1] is also a prefix
        sage: s = WordMorphism('a->Ab,b->Ac,c->A,A->aB,B->aC,C->a')
        sage: balanced_pair_algorithm(s)
        False

        # non terminating example from "A generalized balanced pair algorithm" by Brian F. Martensen
        sage: s = WordMorphism('1->1234,2->124,3->13234,4->1324')
        sage: has_pure_discrete_spectrum(s)  # not tested
    """
    # find a power of s that have fixed point
    p = 1
    while (len((s**p).fixed_points()) == 0):
        p += 1
    s = s**p
    # define w is not
    if w is None:
        w = s.fixed_points()[0][:1]
        if verb > 0:
            print("w = " + str(w))
    else:
        w = Word(w, alphabet=s.domain().alphabet())
    # define pv if not
    if pv is None:
        m = s.incidence_matrix()
        if verb > 1:
            print("incidence matrix:")
            print(m)
        _, pv = getV(m)
        if verb > 1:
            print("pv = %s" % pv)
    # compute the first set of balanced pairs
    to_see = first_balanced_pairs(s, w, pv, verb-1)
    # stabilize by the substitution
    lb = {(u,v):i for i,(u,v) in enumerate(to_see)} # associate an integer to each balanced pair
    n = len(lb)
    ee = dict() # list of entering edges of the graph, for each state, labeled by integers
    while len(to_see) > 0:
        if stop_event is not None and stop_event.is_set():
            return
        u,v = to_see.pop()
        if verb > 1:
            txt1 = "s(" + str(u) + ") = "
            txt2 = " (" + str(v) + ")   "
        for u2,v2 in decompose(s(u), s(v), pv):
            if verb > 1:
                txt1 += "(" + str(u2) + ")"
                txt2 += "(" + str(v2) + ")"
            if (u2,v2) not in lb:
                lb[(u2,v2)] = n
                to_see.add((u2,v2))
                n += 1
            if verb > 2:
                print("%s --> %s (%s --> %s)" % (lb[(u,v)], lb[(u2,v2)], (u,v), (u2,v2)))
            if lb[(u2,v2)] not in ee:
                ee[lb[(u2,v2)]] = set()
            ee[lb[(u2,v2)]].add(lb[(u,v)])
        if verb > 1:
            print(txt1)
            print(txt2)
    if verb > 0:
        print("balanced pairs =")
        print(lb)
        print("ee =")
        print(ee)
    if getgraph:
        return lb, ee
    if getbp:
        return set(lb)
    # browse the graph to determine if every pair leads to a coincidence
    to_see = [lb[(u,v)] for u,v in lb if len(u) == 1 and u == v] # list of coincidences
    seen = set(to_see)
    while len(to_see) > 0:
        e = to_see.pop()
        if e not in ee:
            continue
        for e2 in ee[e]:
            if e2 not in seen:
                seen.add(e2)
                to_see.append(e2)
    pd = len(seen) == len(lb) # pure discreteness
    if verb > 1:
        print("Algo finished !")
    return pd

def check_dimension(s, d, verb=0, stop_event=None):
    """
    Check that the set of eigenvalues is big enough to have pure discrete spectrum
    
    INPUT:
        - ``s`` - WordMorphism
        - ``d`` - degree of Perron eigenvalue of s
        - ``verb`` - int (default: ``0``) -- if > 0, print informations
    """
    if d == 1:
        if verb > 0:
            print("Perron eigenvalue is an integer, compute eigenvalues...")
        # compute the set of eigenvalues
        eigs = morphic_eigenvalues(s)
        if eigs == ZZ:
            if verb > 0:
                print(" -> weakly mixing thus non purely discrete")
            return False
        try:
            if eigs.d == 1:
                print(" -> finite number of rational eigenvalues thus non purely discrete")
                return False
        except:
            pass
    else:
        # compute the dimension of the Q-vector space generated by eigenvalues
        de = dimension_eigenvalues(s)
        if verb > 0:
            print("dimension eigenvalues :", de)
        if de < d:
            if verb > 0:
                print("not enough eigenvalues to have pure discrete spectrum : %s < %s" % (de, d))
            return False
    return True

import multiprocessing, time

def worker(f, args, C, stop_event, result_queue, verb):
    """
    Function used by has_pure_discrete_spectrum() to execute the balanced pair algorithm in parallel with several words
    """
    res = f(*args, stop_event=stop_event)
    if res is not None:
        w = args[1]
        if w in ZZ: # check_dimension
            if res:
                if verb > 0:
                    print("test of eigenvalues terminated but unconclusive")
                return
            else:
                if verb > 0:
                    print("test of eigenvalues terminated conclusively")
                stop_event.set()  # tell to other processes to stop
                result_queue.put(False)  # send result
                return
        # balanced pair alogorithm 
        if res or (C*vector((w+w[:1]).abelian_vector())).is_zero():
            if verb > 0:
                print("balanced pair algorithm terminated conclusively with w =", w)
            stop_event.set()  # tell to other processes to stop
            result_queue.put(res)  # send result

def stopper(processes):
    """
    Function used by has_pure_discrete_spectrum() to stop processes
    """
    time.sleep(1) # wait to let time to processes to finish by themsleves
    print(processes)
    for p in processes:
        if p.is_alive():
            p.terminate()  # kill process

def getV(m):
    """
    Return a matrix in ZZ whose right-kernel is the same as the Perron left-eigenvector

    INPUT:
        - m - matrix with rational coefficients

    OUTPUT:
        A matrix with base_ring ZZ

    EXAMPLES::
        sage: from eigenmorphic.balanced_pair_algo import getV
        sage: s = WordMorphism('a->ab,b->ac,c->a')
        sage: m = s.incidence_matrix()
        sage: getV(m)
        (
                            [1 0 0]
                            [0 1 0]
        1.839286755214161?, [0 0 1]
        )
    """
    b, vp, _ = max(m.eigenvectors_left())
    vp = vp[0]
    K = NumberField(b.minpoly(), 'b', embedding=b)
    vp = vector((K(t) for t in vp))
    m = matrix([list(t) for t in vp]).transpose()
    E = VectorSpace(QQ, m.ncols())
    m = matrix(E.subspace(m).basis())
    d = lcm((c.denom() for c in m.coefficients()))
    return b, matrix(m*d, base_ring=ZZ)

def has_pure_discrete_spectrum(s, nprocs=4, check_dim=True, verb=0):
    """
    Test if the subshift of s has pure discrete spectrum.

    INPUT:
        - ``s`` - WordMorphism -- the substitution (assumed to be primitive)
        - ``nprocs`` - int (default: 4) -- number of words w tested simultaneously
        - ``check_dim`` - bool (default: ``True``) -- if True, test if there are enough eigenvalues to have pure dicrete spectrum
        - ``verb`` - int (default: ``0``) -- If > 0, print informations

    OUTPUT:
        A bool.

    EXAMPLES::
        sage: from eigenmorphic import *
        sage: s = WordMorphism('a->ab,b->ac,c->a')
        sage: has_pure_discrete_spectrum(s)
        True
        sage: s = WordMorphism('a->Ab,b->A,A->aB,B->a')
        sage: has_pure_discrete_spectrum(s)
        False
        sage: s = WordMorphism('1->31,2->412,3->312,4->412')
        sage: has_pure_discrete_spectrum(s)
        True
        sage: s = WordMorphism('a->Ab,b->Ac,c->A,A->aB,B->aC,C->a')
        sage: has_pure_discrete_spectrum(s)
        True

        # non terminating example for the balanced pair alogorithm
        # from "A generalized balanced pair algorithm" by Brian F. Martensen
        # the computation of eigenvalues shows it is weakly mixing 
        sage: s = WordMorphism('1->1234,2->124,3->13234,4->1324')
        sage: has_pure_discrete_spectrum(s)
        False
    """
    # compute pv
    m = s.incidence_matrix()
    if verb > 1:
        print("incidence matrix:")
        print(m)
    b, pv = getV(m)
    if verb > 1:
        print("pv =")
        print(pv)
    # compute coboundary space, to test condition on word in case of False result
    C = coboundary_basis(s)
    # find a power of s that have fixed point
    p = 1
    while (len((s**p).fixed_points()) == 0):
        p += 1
    s = s**p
    # create multiprocessing tools
    stop_event = multiprocessing.Event()  # shared event to indicate to stop
    result_queue = multiprocessing.Queue()  # to get results
    # list of processes
    processes = []

    if check_dim:
        if verb > 0:
            print("test if there are enough eigenvalues...")
        #futures[executor.submit(check_dimension, s, b.minpoly().degree(), verb)] = Word([], alphabet=s.domain().alphabet())
        p = multiprocessing.Process(target=worker, args=(check_dimension, (s, b.minpoly().degree(), verb), C, stop_event, result_queue, verb))
        p.start()
        processes.append(p)
    for n in range(1,1000): # browse possible lengths
        if verb > 1:
            print("test with prefixes of length %s" % n)
        sw = set()
        for w in s.fixed_points():
            sw.add(w[:n])
        if verb > 1:
            print(sw)
        for w in sw:
            # submit a new task
            if verb > 0:
                print("execute balanced_pair_algorithm with w = %s..." % w)
            #futures[executor.submit(balanced_pair_algorithm, s, w, pv)] = w
            p = multiprocessing.Process(target=worker, args=(balanced_pair_algorithm, (s, w, pv), C, stop_event, result_queue, verb))
            p.start()
            processes.append(p)
            while len(processes) == nprocs:
                # remove processes that terminates
                processes2 = []
                for p in processes:
                    if p.is_alive():
                        processes2.append(p)
                processes = processes2
                # get result and force processes to stop
                if stop_event.is_set():
                    return result_queue.get()
                time.sleep(.1)

