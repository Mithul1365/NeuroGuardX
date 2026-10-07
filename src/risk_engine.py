import time


class RiskEngine:

    def __init__(self):

        self.eye_start = None
        self.head_start = None
        self.face_start = None

        # Prevent repeated risk from the same yawn
        self.yawn_active = False

    def update(self, ear, head, yawn, face, perclos):

        current_time = time.time()

        # -----------------------
        # Variables
        # -----------------------

        risk = 0

        eye_closed = False
        head_down = False

        eye_time = 0
        head_time = 0

        # -----------------------
        # Eyes
        # -----------------------

        if ear <= 0.16:

            eye_closed = True

            if self.eye_start is None:
                self.eye_start = current_time

            eye_time = current_time - self.eye_start

        else:

            self.eye_start = None

        # -----------------------
        # Head Pose
        # -----------------------

        if head == "DOWN":

            head_down = True

            if self.head_start is None:
                self.head_start = current_time

            head_time = current_time - self.head_start

        else:

            self.head_start = None

        # -----------------------
        # Yawning
        # -----------------------

        if yawn == "YES":

            # Add risk only once
            # for one continuous yawn
            if not self.yawn_active:

                risk += 3

                self.yawn_active = True

        else:

            self.yawn_active = False

        # -----------------------
        # Face Missing
        # -----------------------

        if face == "MISSING":

            risk += 10

        # -----------------------
        # PERCLOS
        # -----------------------

        # PERCLOS is only a supporting
        # risk indicator.
        # It cannot directly create CRITICAL.

        if eye_closed:

            if perclos >= 60:

                risk += 10

            elif perclos >= 40:

                risk += 5

            elif perclos >= 25:

                risk += 2

        # -----------------------
        # Eye Closure Risk
        # -----------------------

        # 3 seconds or more
        # = WARNING-level risk

        if eye_closed and eye_time >= 3:

            risk += 35

        # -----------------------
        # Head Down Risk
        # -----------------------

        # Head DOWN by itself does not
        # create CRITICAL.

        if head_down and head_time >= 5:

            risk += 10

        # -----------------------
        # Combination Risk
        # -----------------------

        # Long eye closure + head DOWN
        # = strong additional risk

        if eye_closed and eye_time >= 3 and head_down:

            risk += 50

        # Eye closure + yawn

        if eye_closed and yawn == "YES":

            risk += 5

        # Head down + yawn

        if head_down and yawn == "YES":

            risk += 3

        # -----------------------
        # Limit Risk
        # -----------------------

        risk = min(risk, 100)

        # -----------------------
        # FINAL STATUS
        # -----------------------

        # CRITICAL ONLY WHEN:
        #
        # Eyes closed >= 3 sec
        # AND
        # Head DOWN

        if eye_closed and eye_time >= 3 and head_down:

            status = "CRITICAL"

        # WARNING:
        #
        # Eyes closed >= 3 sec

        elif eye_closed and eye_time >= 3:

            status = "WARNING"

        # Otherwise SAFE

        else:

            status = "SAFE"

        return risk, status