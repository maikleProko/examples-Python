import math
import matplotlib.pyplot as plt
import numpy
import time

eps = 0.0001
numberOfPoints = 1000

squareSize = 4

max_value = 9
searched_value = 6

directions = [
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1)
]


# Equation
# curveFunction(x, y) = 1
def curve_function(x_parameter, y_parameter):
    return math.pow(math.fabs(-0.3 + x_parameter), 7 / 2) + math.pow(math.fabs(y_parameter), 7 / 2)


def is_inside(x_parameter, y_parameter):
    return curve_function(x_parameter, y_parameter) - 1 <= 0


def is_on_surface(x_parameter, y_parameter):
    return numpy.isclose(curve_function(x_parameter, y_parameter) - 1, 0, atol=squareSize / numberOfPoints * 2)


def create_new_grid(grid):
    # Copy grid
    new_grid = []
    for j in range(len(grid)):
        new_row = []
        if j != 0 and j != len(grid) - 1:
            y = grid[j][0]
            x_row = grid[j][1]
            for i in range(len(x_row)):
                if i != 0 and i != len(x_row) - 1 and not is_inside(x_row[i][0], y):
                    new_row.append((x_row[i][0], (grid[j - 1][1][i][1] + grid[j + 1][1][i][1] +
                                                  grid[j][1][i + 1][1] + grid[j][1][i - 1][1]) / 4))
                else:
                    new_row.append(grid[j][1][i])
        else:
            for i in range(len(grid[j][1])):
                new_row.append(grid[j][1][i])

        new_grid.append((grid[j][0], new_row))

    return new_grid


def is_stable(new_grid, old_grid, eps_par):
    for j in range(len(new_grid)):
        for i in range(len(new_grid[j][1])):
            old_value = old_grid[j][1][i][1]
            new_value = new_grid[j][1][i][1]

            s = numpy.fabs(old_value - new_value)
            if s > eps_par:
                # print(s)
                return False
    return True


def find_closest_in_grid(value, grid):
    min_diff = numpy.fabs(value - grid[0][1][0][1])
    point = (0, 0)

    for j in range(len(grid)):
        for i in range(len(grid[j][1])):
            x_value_pair = grid[j][1][i]
            if numpy.fabs(value - x_value_pair[1]) < min_diff:
                min_diff = numpy.fabs(value - x_value_pair[1])
                point = (i, j)
    return point


def main():
    startTime = time.time()

    # Create coordinates grid
    grid = []
    for y in numpy.linspace(-squareSize / 2, squareSize / 2, numberOfPoints):
        new_row = []
        for x in numpy.linspace(-squareSize / 2, squareSize / 2, numberOfPoints):
            new_row.append(x)
        grid.append((y, new_row))

    # Init values for grid
    for j in range(len(grid)):
        y = grid[j][0]
        x_row = grid[j][1]
        for i in range(len(x_row)):
            # If border
            if j == 0 or j == len(grid) - 1 or i == 0 or i == len(x_row) - 1:
                x_row[i] = (x_row[i], 0)
            else:
                if is_inside(x_row[i], y):
                    x_row[i] = (x_row[i], max_value)
                else:
                    x_row[i] = (x_row[i], max_value / 2)

    new_grid = create_new_grid(grid)

    counter = 1
    while not is_stable(new_grid, grid, eps):
        grid = new_grid
        new_grid = create_new_grid(grid)
        counter += 1

    grid = new_grid

    # Replace inside with '-100'
    for j in range(len(grid)):
        y = grid[j][0]
        x_row = grid[j][1]
        for i in range(len(x_row)):
            if is_inside(x_row[i][0], y):
                if not is_on_surface(x_row[i][0], y):
                    x_row[i] = (x_row[i][0], -100)

    rectangle = plt.Rectangle((-squareSize / 2, -squareSize / 2), squareSize, squareSize, fc='white', ec='blue',
                              linewidth=3)
    plt.gca().add_patch(rectangle)

    grid_step = squareSize / (numberOfPoints - 1)
    length = 0

    for value in range(1, max_value + 1):
        x_array = []
        y_array = []

        (i_current, j_current) = find_closest_in_grid(value, grid)
        start = (i_current, j_current)
        forbidden_direction = (0, 0)
        point_array = []

        # do_while
        while True:
            # Push point
            point_array.append((i_current, j_current))
            # Find next closest point
            value_array = []
            for direction in directions:
                if (direction != forbidden_direction
                        and (((i_current + direction[0], j_current + direction[1]) not in point_array
                              and j_current > -1 and j_current != len(grid) and i_current > -1
                              and i_current != len(grid)) or (
                                     i_current + direction[0], j_current + direction[1]) == start)):
                    value_array.append(
                        (numpy.fabs(value - grid[j_current + direction[1]][1][i_current + direction[0]][1]),
                         direction))

            if len(value_array) == 0:
                continue

            next_direction = min(value_array)[1]
            i_current += next_direction[0]
            j_current += next_direction[1]

            # Count searched length
            if value == searched_value:
                length += numpy.sqrt(numpy.power(grid_step * next_direction[0], 2)
                                     + numpy.power(grid_step * next_direction[1], 2))

            forbidden_direction = (-next_direction[0], -next_direction[1])

            if (i_current, j_current) == start:
                break

        point_array.append((i_current, j_current))
        for i_j in point_array:
            i = i_j[0]
            j = i_j[1]
            x_array.append(grid[j][1][i][0])
            y_array.append(grid[j][0])

        if value == max_value:
            plt.plot(x_array, y_array, color='blue', linewidth='3')
        else:
            plt.plot(x_array, y_array, color='red')

    print(length)

    plt.axis('equal')
    plt.savefig('./1.png')
    plt.close()


if __name__ == '__main__':
    main()
