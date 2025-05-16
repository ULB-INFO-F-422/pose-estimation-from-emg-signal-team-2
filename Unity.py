from pose_streamer import Pose_Streamer
import pandas as pd
import time
import threading

def send_hand_poses(csv_file, port, freq):
    # Charger les données
    data = pd.read_csv(csv_file).values

    # Créer et démarrer le streamer
    streamer = Pose_Streamer(sfreq=freq, host="127.0.0.1", port=port)
    streamer.start_streaming()

    # Envoyer les poses une par une
    for pose in data:
        streamer.send_pose(pose)
        time.sleep(1.0 / freq)

    # Arrêter le streaming
    streamer.stop_streaming()

def main():
    #csv_file_droite = "freemoves_X.csv" # X
    #csv_file_gauche = "freemoves_y.csv"    # Y
    #csv_file_droite = "guided_X.csv" # X
    #csv_file_gauche = "guided_y.csv"    # Y
    csv_file_droite = "nn_righthand.csv"
    csv_file_gauche = "truepose_lefthand.csv"
    
    freq = 10  # Hz

    # Démarrer deux threads, un pour chaque main
    droite_thread = threading.Thread(target=send_hand_poses, args=(csv_file_droite, 25002, freq))
    gauche_thread = threading.Thread(target=send_hand_poses, args=(csv_file_gauche, 25001, freq))

    droite_thread.start()
    gauche_thread.start()

    droite_thread.join()
    gauche_thread.join()

if __name__ == "__main__":
    main()
