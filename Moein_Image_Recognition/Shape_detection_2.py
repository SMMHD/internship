










def strokeEdges(src, dst, blurKsize = 7, edgeKsize = 5):
   if blurKsize >= 3:
       blurredSrc = cv2.medianBlur(src, blurKsize)
       graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
   else:
       graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
   cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize = edgeKsize)
   normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
   channels = cv2.split(src)
   for channel in channels:
       channel[:] = channel * normalizedInverseAlpha
   cv2.merge(channels, dst)
   
   
   
   
   
   
   
   
   kernel = numpy.array([[-1, -1, -1],
                      [-1, 9, -1],
                      [-1, -1, -1]])
   
   
   
   
   
   
   
   
   cv2.filter2D(src, -1, kernel, dst)
   
   
   
   
   
   
   class VConvolutionFilter(object):
   """A filter that applies a convolution to V (or all of
   BGR)."""

   def __init__(self, kernel):
       self._kernel = kernel

   def apply(self, src, dst):
       """Apply the filter with a BGR or gray
       source/destination."""
       cv2.filter2D(src, -1, self._kernel, dst)

class SharpenFilter(VConvolutionFilter):
   """A sharpen filter with a 1-pixel radius."""

   def __init__(self):
       kernel = numpy.array([[-1, -1, -1],
                             [-1, 9, -1],
                             [-1, -1, -1]])
       VConvolutionFilter.__init__(self, kernel)








class FindEdgesFilter(VConvolutionFilter):
   """An edge-finding filter with a 1-pixel radius."""

   def __init__(self):
       kernel = numpy.array([[-1, -1, -1],
                             [-1, 8, -1],
                             [-1, -1, -1]])
       VConvolutionFilter.__init__(self, kernel)
       
       
       
       
       
       
       
class BlurFilter(VConvolutionFilter):
   """A blur filter with a 2-pixel radius."""

   def __init__(self):
      kernel = numpy.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04],
                             [0.04, 0.04, 0.04, 0.04, 0.04],
                            [0.04, 0.04, 0.04, 0.04, 0.04]])
    VConvolutionFilter.__init__(self, kernel)
       
       
       
       
       
       
       
class EmbossFilter(VConvolutionFilter):
   """An emboss filter with a 1-pixel radius."""

   def __init__(self):
       kernel = numpy.array([[-2, -1, 0],
                             [-1, 1, 1],
                             [ 0, 1, 2]])
       VConvolutionFilter.__init__(self, kernel)
       
       
       
       
       
       
       
       
       
    class EmbossFilter(VConvolutionFilter):
   """An emboss filter with a 1-pixel radius."""

   def __init__(self):
       kernel = numpy.array([[-2, -1, 0],
                             [-1, 1, 1],
                             [ 0, 1, 2]])
       VConvolutionFilter.__init__(self, kernel)
       
       
       
       
       
       
       
import cv2
import filters

from managers import WindowManager, CaptureManager

class Cameo(object):

   def __init__(self):
       self._windowManager = WindowManager('Cameo',
                                           self.onKeypress)
       self._captureManager = CaptureManager(
           cv2.VideoCapture(0), self._windowManager, True)
       self._curveFilter = filters.BGRPortraCurveFilter()
   def run(self):
       """Run the main loop."""
       self._windowManager.createWindow()
       while self._windowManager.isWindowCreated:
           self._captureManager.enterFrame()
           frame = self._captureManager.frame

           filters.strokeEdges(frame, frame)
           self._curveFilter.apply(frame, frame)

           self._captureManager.exitFrame()
           self._windowManager.processEvents()







import cv2
import numpy as np

img = cv2.imread("../images/statue_small.jpg", 0)
cv2.imwrite("canny.jpg", cv2.Canny(img, 200, 300))
cv2.imshow("canny", cv2.imread("canny.jpg"))
cv2.waitKey()
cv2.destroyAllWindows()







import cv2
import numpy as np

img = np.zeros((200, 200), dtype=np.uint8)
img[50:150, 50:150] = 255

ret, thresh = cv2.threshold(img, 127, 255, 0)
image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img = cv2.drawContours(color, contours, -1, (0,255,0), 2)
cv2.imshow("contours", color)
cv2.waitKey()
cv2.destroyAllWindows()









import cv2
import numpy as np

img = cv2.pyrDown(cv2.imread("hammer.jpg", cv2.IMREAD_UNCHANGED))

ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY) , 127, 255, cv2.THRESH_BINARY)
image, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
# find bounding box coordinates
x,y,w,h = cv2.boundingRect(c)
cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)

# find minimum area
rect = cv2.minAreaRect(c)
# calculate coordinates of the minimum area rectangle
box = cv2.boxPoints(rect)
# normalize coordinates to integers
box = np.int0(box)
# draw contours
cv2.drawContours(img, [box], 0, (0,0, 255), 3)
# calculate center and radius of minimum enclosing circle
(x,y),radius = cv2.minEnclosingCircle(c)
# cast to integers
center = (int(x),int(y))
radius = int(radius)
# draw the circle
img = cv2.circle(img,center,radius,(0,255,0),2)

cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
cv2.imshow("contours", img)