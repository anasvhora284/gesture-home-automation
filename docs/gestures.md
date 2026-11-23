# Gestures

| Gesture (class) | Device | Serial command | Relay / pin |
|---|---|---|---|
| okay | All | `OKAY` | all ON |
| stop | All | `STOP` | all OFF |
| smile | Charger ON | `SMILE` | relay_1, D8 -> IN3 |
| live long | Charger OFF | `LIVE_LONG` | relay_1, D8 -> IN3 |
| thumbs up | Fan ON | `THUMBS_UP` | relay_2, D9 -> IN2 |
| thumbs down | Fan OFF | `THUMBS_DOWN` | relay_2, D9 -> IN2 |
| peace | Bulb ON | `PEACE` | relay_3, D10 -> IN1 |
| call me | Bulb OFF | `CALL_ME` | relay_3, D10 -> IN1 |
| fist | Buzzer ON | `FIST` | D11 |
| rock | Buzzer OFF | `ROCK` | D11 |

Commands are ASCII, newline-terminated, 9600 baud.

Note: the original hand-written mapping note listed `live long` as charger ON and `smile` as OFF.
The final code does the opposite (smile = ON); this table follows the code.
