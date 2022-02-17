from n_puzzle import NPuzzle as NP 

new_puzzle = NP(4)
new_puzzle.reset()
new_puzzle.visualise()
print(new_puzzle.read_tile(1,2))
print(new_puzzle.is_solvable())