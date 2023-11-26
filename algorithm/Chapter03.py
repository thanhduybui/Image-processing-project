import numpy as np
import cv2

L = 256


# def Negative(imgin):
#     M, N, C = imgin.shape
#     imgout = np.zeros((M, N), np.uint8)
#     for x in range(0, M):
#         for y in range(0, N):
#             r = imgin[x, y]
#             s = L-1-r
#             imgout[x, y] = s
#     return imgout
def Negative(imgin):
    if len(imgin.shape) == 3:  # Handling a color image (height, width, channels)
        M, N, C = imgin.shape
    elif len(imgin.shape) == 2:  # Handling a grayscale image (height, width)
        M, N = imgin.shape
        C = 1  # Assume one channel for grayscale

    imgout = np.zeros((M, N, C), dtype=np.uint8)
    L = 256  # Assuming 8-bit image (0-255)

    for x in range(M):
        for y in range(N):
            if C == 1:
                r = imgin[x, y]
                s = L - 1 - r
                imgout[x, y] = s
            else:
                for c in range(C):
                    r = imgin[x, y, c]
                    s = L - 1 - r
                    imgout[x, y, c] = s

    return imgout


def Logarit(imgin):

    M, N = imgin.shape[:2]
    imgout = np.zeros((M, N), np.uint8)

    c = (L - 1) / np.log(L)

    # Avoid log(0) by setting zeros to 1
    imgin[imgin == 0] = 1

    # Perform the logarithmic transformation using vectorized operations
    imgout = np.clip(c * np.log(1 + imgin), 0, 255).astype(np.uint8)

    return imgout


def Power(imgin):
    imgout = np.zeros_like(imgin, dtype=np.uint8)
    gamma = 0.9
    c = np.power(255, 1 - gamma)  # Assuming 8-bit image (0-255)

    img_power = c * np.power(imgin.astype(np.float32) / 255.0, gamma) * 255.0
    imgout = np.clip(img_power, 0, 255).astype(np.uint8)

    return imgout


def PiecewiseLinear(imgin, L=256):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)

    # Calculate minimum and maximum values using NumPy
    rmin = np.min(imgin)
    rmax = np.max(imgin)

    s1 = 0
    s2 = L - 1

    # Avoid division by zero
    if rmax != rmin:
        for x in range(0, M):
            for y in range(0, N):
                r = imgin[x, y]
                if r < rmin:
                    s = s1 / rmin * r
                elif r < rmax:
                    s = (s2 - s1) / (rmax - rmin) * (r - rmin) + s1
                else:
                    s = (L - 1 - s2) / (L - 1 - rmax) * (r - rmax) + s2
                imgout[x, y] = np.uint8(s)
    else:
        # Handle the case when rmax equals rmin
        imgout = np.copy(imgin)

    return imgout


def Histogram(imgin):
    if len(imgin.shape) == 2:  # Grayscale image
        M, N = imgin.shape
    elif len(imgin.shape) == 3:  # Color image (RGB/BGR)
        M, N, _ = imgin.shape

    imgout = np.zeros((M, L), np.uint8) + 255
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r]+1
    p = h/(M*N)
    scale = 5000
    for r in range(0, L):
        cv2.line(imgout, (r, M-1), (r, M-1-int(scale*p[r])), (0, 0, 0))
    return imgout


def HistEqual(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    h = np.zeros(L, np.int32)
    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            h[r] = h[r]+1
    p = h/(M*N)

    s = np.zeros(L, np.float64)
    for k in range(0, L):
        for j in range(0, k+1):
            s[k] = s[k] + p[j]

    for x in range(0, M):
        for y in range(0, N):
            r = imgin[x, y]
            imgout[x, y] = np.uint8((L-1)*s[r])
    return imgout


def HistEqualColor(imgin):
    B = imgin[:, :, 0]
    G = imgin[:, :, 1]
    R = imgin[:, :, 2]
    B = cv2.equalizeHist(B)
    G = cv2.equalizeHist(G)
    R = cv2.equalizeHist(R)
    imgout = np.array([B, G, R])
    imgout = np.transpose(imgout, axes=[1, 2, 0])
    return imgout


def LocalHist(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 3
    n = 3
    w = np.zeros((m, n), np.uint8)
    a = m // 2
    b = n // 2
    for x in range(a, M-a):
        for y in range(b, N-b):
            for s in range(-a, a+1):
                for t in range(-b, b+1):
                    w[s+a, t+b] = imgin[x+s, y+t]
            w = cv2.equalizeHist(w)
            imgout[x, y] = w[a, b]
    return imgout


def HistStat(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 3
    n = 3
    w = np.zeros((m, n), np.uint8)
    a = m // 2
    b = n // 2
    mG, sigmaG = cv2.meanStdDev(imgin)
    C = 22.8
    k0 = 0.0
    k1 = 0.1
    k2 = 0.0
    k3 = 0.1
    for x in range(a, M-a):
        for y in range(b, N-b):
            for s in range(-a, a+1):
                for t in range(-b, b+1):
                    w[s+a, t+b] = imgin[x+s, y+t]
            msxy, sigmasxy = cv2.meanStdDev(w)
            r = imgin[x, y]
            if (k0*mG <= msxy <= k1*mG) and (k2*sigmaG <= sigmasxy <= k3*sigmaG):
                imgout[x, y] = np.uint8(C*r)
            else:
                imgout[x, y] = r
    return imgout


def BoxFilter(imgin):
    m = 21
    n = 21
    w = np.ones((m, n))
    w = w/(m*n)
    imgout = cv2.filter2D(imgin, cv2.CV_8UC1, w)
    return imgout


def Threshold(imgin):
    temp = cv2.blur(imgin, (1, 1))
    retval, imgout = cv2.threshold(temp, 215, 255, cv2.THRESH_BINARY)
    return imgout


def MedianFilter(imgin):
    M, N = imgin.shape
    imgout = np.zeros((M, N), np.uint8)
    m = 5
    n = 5
    w = np.zeros((m, n), np.uint8)
    a = m // 2
    b = n // 2
    for x in range(0, M):
        for y in range(0, N):
            for s in range(-a, a+1):
                for t in range(-b, b+1):
                    w[s+a, t+b] = imgin[(x+s) % M, (y+t) % N]
            w_1D = np.reshape(w, (m*n,))
            w_1D = np.sort(w_1D)
            imgout[x, y] = w_1D[m*n//2]
    return imgout


def Sharpen(imgin):
    # Đạo hàm cấp 2 của ảnh
    w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    temp = cv2.filter2D(imgin, cv2.CV_32FC1, w)

    # Hàm cv2.Laplacian chỉ tính đạo hàm cấp 2
    # cho bộ lọc có số -4 chính giữa
    imgout = imgin - temp
    imgout = np.clip(imgout, 0, L-1)
    imgout = imgout.astype(np.uint8)
    return imgout


def Gradient(imgin):
    sobel_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    # Đạo hàm cấp 1 theo hướng x
    mygx = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_x)
    # Đạo hàm cấp 1 theo hướng y
    mygy = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_y)

    # Lưu ý: cv2.Sobel có hướng x nằm ngang
    # ngược lại với sách Digital Image Processing
    gx = cv2.Sobel(imgin, cv2.CV_32FC1, dx=1, dy=0)
    gy = cv2.Sobel(imgin, cv2.CV_32FC1, dx=0, dy=1)

    imgout = abs(gx) + abs(gy)
    imgout = np.clip(imgout, 0, L-1)
    imgout = imgout.astype(np.uint8)
    return imgout
