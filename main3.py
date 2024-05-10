import numpy as np
import tensorflow as tf
import Board
import simpleAiAlgorithm

print("TensorFlow version:", tf.__version__)
rounds = 0
winrate = 0
wins = 0
while winrate < 0.8 or rounds < 100:
    l = lambda x: [Board.Board.boards[i][x] for i in range(len(Board.Board.boards))]
    (x_train, y_train) = np.array(l(0)), np.array(l(1))

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(8, 8)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1)
    ])
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
                  loss=loss_fn,
                  metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=5, verbose=0)
    board = Board.Board()
    replay = []
    while not board.is_game_ended():
        boards = np.array(board.get_all_possible_boards(1))
        probabilities = model.predict(boards, verbose=0)
        index_of_max_probability = np.argmax(probabilities)
        board_with_highest_win_probability = boards[index_of_max_probability]
        board.board = board_with_highest_win_probability
        if board.is_game_ended():
            break
        board.turn(simpleAiAlgorithm.best_turn(board, 2))
        replay.append(board.board)

    rounds += 1
    win = board.is_there_color(1)
    wins += win
    winrate = wins / rounds
    for board in replay:
        Board.Board.boards.append((board, win))

    # for board in replay:
    #     for line in board:
    #         print(*line)
    #     print("\n")
    print(f"Winrate = {winrate}; Round = {rounds}")
print("The end!")
