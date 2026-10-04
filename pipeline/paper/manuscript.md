# A restricted Euclidean TSP heuristic for structured geometric instances

## Abstract

This manuscript presents a lightweight heuristic solver for Euclidean TSP instances on structured geometric inputs. The method is intentionally not framed as a general polynomial-time exact solution to the unrestricted TSP. Instead, it is designed as a paper-ready prototype for a restricted problem class where geometric structure and input regularity are exploited. The algorithm combines a nearest-neighbor construction phase with a 2-opt local improvement step. The goal is to provide a scientifically consistent method for a limited domain, while explicitly avoiding overgeneralization beyond the geometric assumptions of the model.

## 1. Introduction

The traveling salesman problem is a classical optimization problem with deep connections to complexity theory and combinatorial optimization. In its unrestricted form, the TSP is defined over a complete weighted graph and seeks a minimum-weight Hamiltonian cycle. In contrast, Euclidean TSP instances are defined on points in the plane with distances given by the Euclidean metric. This special case is widely studied and has a different theoretical and empirical profile from the unrestricted weighted version.

This work does not claim a polynomial-time exact algorithm for the unrestricted TSP. Instead, it focuses on a restricted Euclidean setting in which the input geometry is regular enough to support a transparent and implementable heuristic. The aim is to provide a coherent paper-level prototype that can be evaluated experimentally and discussed rigorously.

## 2. Problem setting

We consider a set of points P = {p1, ..., pn} in R^2. A tour is a permutation of the points, and its length is the sum of Euclidean distances between consecutive points. The objective is to find a Hamiltonian cycle of minimum total length:

$$
T^* = \arg\min_{T} \sum_{(i,j) \in T} \|p_i - p_j\|_2.
$$

The formulation is standard for the Euclidean TSP, but the proposed method is intentionally limited to structured geometric instances rather than all possible complete graphs or arbitrary weight matrices.

## 3. Assumptions and scope

The method is based on the following assumptions:

- Euclidean input in the plane;
- complete graph over the points;
- distance defined by the standard Euclidean norm;
- structured or moderately regular geometric data;
- emphasis on practical solution quality rather than general exactness.

These assumptions define the scientific scope of the method. The algorithm is not meant to be universal, but rather to provide a critical and realistic prototype for a special class of TSP instances.

## 4. Proposed method

The algorithm consists of two phases: nearest-neighbor construction followed by 2-opt local refinement.

### 4.1 Initial construction

Starting from an arbitrary seed point, the method repeatedly selects the unvisited point closest to the current one and appends it to the tour. The resulting tour is feasible but not necessarily optimal.

### 4.2 Local improvement

The 2-opt phase inspects pairs of edges in the tour and reverses the segment between them whenever the reversal decreases the total length. This procedure is repeated until no further local improvement is found.

### 4.3 Pseudocode

```text
Input: set of points P = {p1, ..., pn} in R^2
Output: Hamiltonian cycle T

1. S <- {p1, ..., pn}
2. T <- []
3. current <- arbitrary starting point in S
4. while S \ {current} is nonempty:
5.     next <- nearest unvisited point to current
6.     append next to T
7.     current <- next
8. end while
9. append initial point to close the cycle
10. improved <- true
11. while improved:
12.     improved <- false
13.     for each pair of edges (i, j), (k, l) in T:
14.         if reversing the segment between j and k reduces total length:
15.             reverse that segment
16.             improved <- true
17.         end if
18.     end for
19. end while
20. return T
```

## 5. Complexity and validity

The nearest-neighbor build phase is straightforward to implement and can be analyzed in standard algorithmic terms, while the 2-opt improvement stage performs a sequence of local evaluations. The key point, however, is that this is a heuristic design for a restricted geometric domain. It does not establish polynomial-time exactness for the unrestricted TSP and should not be interpreted as such.

## 6. Experimental protocol

The solver can be evaluated on synthetic Euclidean instances of varying sizes and structures. Candidate benchmarks include:

- uniformly random points in a square;
- clustered inputs;
- grid-like or highly regular points;
- increasing instance sizes for scaling analysis.

For each instance, we can record tour length, runtime, and the number of successful 2-opt improvements. These measures are useful for understanding the behavior of the method under the geometric assumptions specified above.

## 7. Discussion

The method has practical value because it is easy to describe, cheap to implement, and transparent in its behavior. Its main scientific strength is that it is honest about its scope: it is a restricted-domain heuristic rather than a universal exact solver.

The method also has clear limitations. It does not produce optimal tours for arbitrary weighted graphs, and its performance depends on the geometry of the input. This is not a weakness of the design so much as a statement of the problem class it addresses.

## 8. Conclusion

This manuscript presents a coherent prototype for a restricted Euclidean TSP setting. The algorithm is intentionally framed as a structured, empirically evaluable heuristic, not as a claim of general polynomial-time exactness. The value of the contribution lies in the clarity of the assumptions, the transparency of the method, and the explicit distinction between special-case solvability and general-case hardness.
