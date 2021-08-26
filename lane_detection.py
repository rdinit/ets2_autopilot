import numpy as np
import cv2

class LaneDetection():
    last_lane = []
    def get_steering_by_image(self, img, bbox=(0,0,1440,940), last_lane=[], draw=False):
        if last_lane == []:
            last_lane = self.last_lane
        dst = np.float32([[0, 300], [200, 300], [200, 0], [0, 0]])
        src = np.float32([[490, 490], #координаты точек трапеции
                    [800, 490],
                    [890, 530],
                    [420, 530]])
        img = img.crop(box=bbox)
        #img = ImageGrab.grab(bbox=(0,40,1440,940))
        #img = Image.open('test1.png')
        frame = np.array(img)
        #v_min = cv2.getTrackbarPos("Hue", WINDOWNAME)
        v_min = 190
        connectivity = 4

        image = frame
        M = cv2.getPerspectiveTransform(src=src, dst=dst)
        cvt_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        warped_c = cv2.warpPerspective(frame, M, (360, 200), flags=cv2.INTER_LINEAR)
        
        # побитово складываем оригинальную картинку и маску
        
        cropped = warped_c[50:190, 150:380]
        cropped_v = list(map(lambda x: [i[2] for i in x], cropped))

        asphalt_bright = np.average(cropped_v)

        v_min = ((3 / 5) * asphalt_bright ) + 120
        
        thresh = cv2.inRange(cvt_image, (0, 0, v_min), (255, 255, 255))
        image = cv2.bitwise_and(image, image, mask=thresh)
        warped = cv2.warpPerspective(thresh, M, (360, 200), flags=cv2.INTER_LINEAR)
        
        
        output = cv2.connectedComponentsWithStats(warped, connectivity, cv2.CV_32S)
        stat = output[2]
        lane_elements = []
        for element in stat[1:]:
            start_point = (element[0], element[1])
            end_point = (element[0] + element[2], element[1] + element[3])

            warped = cv2.rectangle(warped, start_point, end_point, (0, 255 ,0), thickness=3)
            color = (0, 0, 255)
            if element[2] < 30 and element[0] < 180 and element[3] > 180:
                if last_lane != []:
                    dx = abs(last_lane[0] - element[0])
                    dy = abs(last_lane[1] - element[1])
                    d = (dx ** 2 + dy ** 2) ** 0.5
                else:
                    d = 0
                color = (0, 255, 0)
                lane_elements.append([*element.copy(), d])
            warped_c = cv2.rectangle(warped_c, start_point, end_point, color, thickness=3)

        lane_elements.sort(key=lambda x: x[-1])
        text = 'left'
        if len(lane_elements) == 0:
            text = 'left'
        elif lane_elements[0][-1] < 40 or len(lane_elements) == 1:
            start_point = (lane_elements[0][0], lane_elements[0][1])
            end_point = (lane_elements[0][0] + lane_elements[0][2], lane_elements[0][1] + lane_elements[0][3])
            
            #warped_c = cv2.rectangle(warped_c, start_point, end_point, (0, 0 ,255), 3)
            last_lane = list(start_point)
            #print(last_lane)
            x = lane_elements[0][0]
            #print(lane_elements)
            if x < 50:
                text = 'left'
                if x < 30:
                    text = 'vleft'
            elif x > 70:
                text = 'right'
                if x > 90:
                    text = 'vright'
            else:
                text = 'center'
            if draw:
                warped_c = cv2.rectangle(warped_c, start_point, end_point, (255, 0, 255), thickness=3)
        if draw:
            cv2.putText(warped_c, text, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
            cv2.imshow("warped color", warped_c)
            cv2.imshow("warped filter", warped)
            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
        self.last_lane = last_lane.copy()
        return text
