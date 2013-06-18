import numpy as np

def get_harr_matrix(N):
    K = np.ceil(np.log(N) / np.log(2.)).astype(int)
    NN = 2 ** K
    W = np.zeros((NN, NN))
    j = 0
    for k in range(K + 1):
        print k
        if k == 0:
            W[j, :] = 1.
            j += 1
            continue
        l = 2 ** (K - k)
        for p in range(2 ** (k - 1)):
            print k, l, p, j
            W[j, 2 * p * l: 2 * p * l + l] = 1.
            W[j, 2 * p * l + l: 2 * p * l + 2 * l] = -1.
            j += 1
    return W[0:N, 0:N] / np.sqrt(np.sum(W * W, axis=1))[:,None]

def test_matrix(W):
    tiny = 1.e-8
    n1, n2 = W.shape
    for i in range(n1):
        for j in range(n2):
            d1 = np.dot(W[i, :], W[j, :])
            d2 = np.dot(W[:, i], W[:, j])
            print i, j, d1, d2
            if i == j:
                if (d1 - 1.) ** 2 > tiny or (d2 - 1.) ** 2 > tiny:
                    print "FAIL"
                    return False
            if i != j:
                if d1 ** 2 > tiny or d2 ** 2 > tiny:
                    print "FAIL"
                    return False
    return True

if __name__ == "__main__":
    W = get_harr_matrix(2 ** 16)
    print W.shape
