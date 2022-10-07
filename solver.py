"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

=== Module Description ===

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue
from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


# Your solve method MUST be a recursive function (i.e. it must make
# at least one recursive call to itself)
# You may NOT change the interface to the solve method.
class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.

    ==== Doctest Code ====
    >>> from sudoku_puzzle import SudokuPuzzle
    >>> s = SudokuPuzzle(4, [[" ", " ", "B", " "],
    ...                      ["B", " ", "D", "C"],
    ...                      [" ", " ", "A", " "],
    ...                      [" ", " ", "C", " "]],
    ...                  {"A", "B", "C", "D"})
    >>> solver = DfsSolver()
    >>> solution = solver.solve(s)
    >>> actual = solution[-1]
    >>> expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
    ...                             ["B", "A", "D", "C"],
    ...                             ["D", "C", "A", "B"],
    ...                             ["A", "B", "C", "D"]],
    ...                         {"A", "B", "C", "D"})
    >>> actual == expected
    True
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        result = [puzzle]
        if puzzle.is_solved():
            return result
        if seen is None:
            seen = {str(puzzle)}
        else:
            seen.add(str(puzzle))
        for choice in puzzle.extensions():
            if str(choice) not in seen and not choice.fail_fast():
                result.extend(self.solve(choice, seen))
                if result[-1].is_solved():
                    return result
        return []


# Hint: You may find a Queue useful here.
class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.

    ==== Doctest Code ====
    >>> from sudoku_puzzle import SudokuPuzzle
    >>> s = SudokuPuzzle(4, [[" ", " ", "B", " "],
    ...                      ["B", " ", "D", "C"],
    ...                      [" ", " ", "A", " "],
    ...                      [" ", " ", "C", " "]],
    ...                  {"A", "B", "C", "D"})
    >>> solver = BfsSolver()
    >>> solution = solver.solve(s)
    >>> actual = solution[-1]
    >>> expected = SudokuPuzzle(4, [["C", "D", "B", "A"],
    ...                             ["B", "A", "D", "C"],
    ...                             ["D", "C", "A", "B"],
    ...                             ["A", "B", "C", "D"]],
    ...                         {"A", "B", "C", "D"})
    >>> actual == expected
    True
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if puzzle.is_solved():
            return [puzzle]
        q = Queue()
        if seen is None:
            seen = set()
        for next_step in puzzle.extensions():
            q.enqueue([puzzle, next_step])
        while not q.is_empty():
            first = q.dequeue()

            if first[-1].is_solved() and str(first[-1]) not in seen:
                return first

            if not first[-1].fail_fast() and str(first[-1]) not in seen:
                seen.add(str(first[-1]))
                for next_choice in first[-1].extensions():
                    temp = first[:]
                    temp.append(next_choice)
                    q.enqueue(temp)

        return []


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
