(import [pandas :as pd])
(import [numpy :as np])

(setv path "../../logs/log.csv")
(setv data (pd.read_csv path))

(setv score (get data "score"))
(print "Score variance:" (.var score))

(setv time (get data "time"))
(print "Time mean:" (.mean time))