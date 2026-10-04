# A restricted Euclidean TSP heuristic for structured geometric instances

## Abstract

This manuscript presents a lightweight heuristic solver for Euclidean TSP instances on structured geometric inputs. The method is intentionally not framed as a general polynomial-time exact solution to the unrestricted TSP. Instead, it is designed as a paper-ready prototype for a restricted problem class where geometric structure and input regularity are exploited.

## Problem setting

We consider a complete graph over Euclidean points in the plane. The objective is to find a Hamiltonian cycle minimizing the total travel length.

## Proposed method

The algorithm combines:

- nearest-neighbor tour construction;
- 2-opt local optimization;
- a restricted geometric interpretation of the input.

This yields a practical approximation heuristic for structured Euclidean instances.

## Experimental protocol

We evaluate the solver on synthetic Euclidean points of varying size, recording tour length and runtime behavior.

## Discussion

The method does not generalize to arbitrary weighted complete graphs, and does not claim polynomial-time exactness for the unrestricted TSP. It instead demonstrates a realistic paper-level algorithmic design for a restricted subclass of the problem.
