import numpy as np
from sklearn import datasets, svm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def main():
    # Import iris data
    iris = datasets.load_iris()
    x = iris.data[:, :2]  # take the first two features.
    y = iris.target  # label

    # Splitting data into train, validation and test set
    # 50% training set, 20% validation set, 30% test set
    x_train, x_tmp, y_train, y_tmp = train_test_split(x, y, test_size=0.5, random_state=42)
    x_validate, x_test, y_validate, y_test = train_test_split(x_tmp, y_tmp, test_size=0.4, random_state=42)

    c = [10**(-3), 10**(-2), 10**(-1), 10**0, 10**1, 10**2, 10**3]
    g = [10**(-9), 10**(-7), 10**(-5), 10**(-3)]
    #c = [10**(-2), 10**(-1), 10**0, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10]
    #g = [10**(-9), 10**(-8), 10**(-7), 10**(-6), 10**(-5), 10**(-4), 10**(-3), 10**(-2), 10**(-1), 10**0, 10**1, 10**2, 10**3]
    best_values = [-1, -1, -1]  # respectively best success rate, best C and best gamma
    a = []  # rows are C values and columns are gamma values, each cell is the accuracy for the corresponding C and gamma

    plt.figure('SVC with rbf-kernel', figsize=(30, 20))
    k = 1
    for i in c:
        values = []
        for j in g:
            clf = svm.SVC(kernel='rbf', C=i, gamma=j)
            clf.fit(x_train, y_train)

            # create a mesh to plot in
            x_min, x_max = x_train[:, 0].min() - 1, x_train[:, 0].max() + 1
            y_min, y_max = x_train[:, 1].min() - 1, x_train[:, 1].max() + 1
            h = (x_max / x_min) / 100
            xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

            z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
            z = z.reshape(xx.shape)

            plt.subplot(len(c), len(g), k)
            title = 'C=' + str(i) + ' and gamma=' + str(j)
            plt.title(title, fontsize=30)
            plt.contourf(xx, yy, z, cmap=plt.get('Paired'), alpha=0.8)
            plt.scatter(x_train[:, 0], x_train[:, 1], c=y_train, cmap=plt.get('Paired'))
            plt.xlim(xx.min(), xx.max())

            print('With C=' + str(i) + ' and gamma=' + str(j))
            full_prediction = clf.predict(x_validate)
            print('[-] Number of mislabeled points out of a total %d points: %d'
                  % (len(y_validate), (y_validate != full_prediction).sum()))
            accuracy = (100 * (len(y_validate) - (y_validate != full_prediction).sum())) / len(y_validate)
            print('[-] With an accuracy of %.3f%s'
                  % (accuracy, '%'))

            if accuracy > best_values[0]:
                best_values = accuracy, i, j

            k += 1
            values.append(accuracy)

        a.append(values)
    plt.show()
    plt.close()

    # 2D heatmap validation accuracy
    plt.title('Validation Accuracy')
    plt.xlabel('gamma')
    plt.ylabel('C')
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()
    plt.close()

    print('\nBest C=' + str(best_values[1]) + ' and best gamma=' + str(best_values[2]))

    # With the best C and gamma evaluating test set
    print('Evaluating test set')
    clf = svm.SVC(kernel='rbf', C=best_values[1], gamma=best_values[2])
    clf.fit(x_train, y_train)

    x_min, x_max = x_train[:, 0].min() - 1, x_train[:, 0].max() + 1
    y_min, y_max = x_train[:, 1].min() - 1, x_train[:, 1].max() + 1
    h = (x_max / x_min) / 100
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    title = 'C=' + str(best_values[1]) + ' and gamma=' + str(best_values[2])
    plt.title(title, fontsize=20)
    plt.contourf(xx, yy, z, cmap=plt.get('Paired'), alpha=0.8)
    plt.scatter(x_train[:, 0], x_train[:, 1], c=y_train, cmap=plt.get('Paired'))
    plt.xlim(xx.min(), xx.max())

    full_prediction = clf.predict(x_test)
    print('[-] Number of mislabeled points out of a total %d points: %d'
          % (len(y_test), (y_test != full_prediction).sum()))
    print('[-] With an accuracy of: %.3f%s'
          % ((100 * (len(y_test) - (y_test != full_prediction).sum())) / len(y_test), '%'))

    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
