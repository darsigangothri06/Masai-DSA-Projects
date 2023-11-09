import random
from collections import deque
from colorama import Fore, Style, init

init(autoreset=True)

# Constants
WALL = Fore.RED + '▓' + Style.RESET_ALL
OPEN_SPACE = '◌' + Style.RESET_ALL
START = Fore.GREEN + 'S' + Style.RESET_ALL
END = Fore.GREEN + 'E' + Style.RESET_ALL
PATH = Fore.GREEN + '◍' + Style.RESET_ALL

# To mark the path on maze
def mark_solution(maze, path):
    for px, py in path:
        maze[py][px] = PATH

# Generate a maze
def create_solvable_maze(size):
    maze = [[WALL] * size for _ in range(size)]
    stack = [(1, 1)]
    while stack:
        current_x, current_y = stack[-1]
        maze[current_y][current_x] = OPEN_SPACE

        # Exploring all directions
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        found = False
        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy
            if 0 < new_x < size and 0 < new_y < size and maze[new_y][new_x] == WALL:
                maze[current_y + dy // 2][current_x + dx // 2] = OPEN_SPACE
                stack.append((new_x, new_y))
                found = True
                break

        if not found:
            stack.pop()
    
    maze[0][1] = START
    maze[size - 1][size - 2] = END
    return maze

# Print the maze
def display_maze(maze):
    size = len(maze)
    maze[0][1] = START
    maze[size - 1][size - 2] = END
    for row in maze:
        print(Fore.RED + "+" + "---+" * len(row))
        print("| " + " | ".join(row) + " | ")
    print(Fore.RED + "+" + "---+" * len(maze[0]))

# Finding solution using Matrix DFS
def find_solution_path(maze):
    stack = deque([(1, 0)])
    visited = set()

    while stack:
        current_x, current_y = stack[-1]

        if current_x == len(maze[0]) - 2 and current_y == len(maze) - 1:
            return stack

        found = False
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = current_x + dx, current_y + dy
            if (0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and 
                maze[new_y][new_x] != WALL and (new_x, new_y) not in visited):
                stack.append((new_x, new_y))
                visited.add((new_x, new_y))
                found = True
                break

        if not found:
            stack.pop()

    return None

# Main function
def main():
    maze_size = int(input("Enter the size of the maze (n x n): "))
    maze = create_solvable_maze(maze_size)
    print("Generated Maze:")
    display_maze(maze)
    
    while True:
        user_choice = input("\n1. Print Solution\n2. Generate another puzzle\n3. Exit the Game\nEnter your choice (1/2/3): ")
        if user_choice == '1':
            solution_path = find_solution_path(maze)
            if solution_path:        
                mark_solution(maze, solution_path)
                print("Maze with Path:")
                display_maze(maze)
                maze_size = int(input("Enter the size of the maze (n x n): "))
                maze = create_solvable_maze(maze_size)
                print("Generated Maze:")
                display_maze(maze)
            else:
                print("No solution path found.")
        elif user_choice == '2':
            maze_size = int(input("Enter the size of the maze (n x n): "))
            maze = create_solvable_maze(maze_size)
            print("Generated Maze:")
            display_maze(maze)
        elif user_choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
