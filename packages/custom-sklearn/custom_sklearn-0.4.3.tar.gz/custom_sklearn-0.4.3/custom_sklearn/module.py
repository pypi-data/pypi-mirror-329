def custom_sklearn():
    print( """
        import numpy as np
        from sklearn.datasets import make_classification
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import KFold, LeaveOneOut, GridSearchCV
        from sklearn.metrics import accuracy_score, adjusted_rand_score
        from sklearn.linear_model import LinearRegression, LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.svm import SVC
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.naive_bayes import GaussianNB
        from sklearn.cluster import KMeans, DBSCAN
        from sklearn.decomposition import PCA

        # For k-medoids clustering (requires scikit-learn-extra)
        try:
            from sklearn_extra.cluster import KMedoids
        except ImportError:
            print("sklearn_extra is not installed. k-medoids clustering function will be skipped.")
            KMedoids = None


        def decision_tree_classifier():
            print("=== Decision Tree Classifier ===")
            # Generate synthetic dataset
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # 10-fold cross-validation
            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            fold_accuracies = []

            for fold, (train_index, test_index) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_index], X_scaled[test_index]
                y_train, y_test = y[train_index], y[test_index]

                model = DecisionTreeClassifier(max_depth=3, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                fold_accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")

            print(f"Average Accuracy: {np.mean(fold_accuracies):.2f}\n")


        def elbow_method():
            print("=== Elbow Method (using KMeans inertia) ===")
            # Use only features from synthetic data (ignore labels)
            X, _ = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            inertias = {}
            for k in range(1, 11):
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(X_scaled)
                inertias[k] = kmeans.inertia_
                print(f"k = {k}, Inertia = {kmeans.inertia_:.2f}")
            print("Elbow method values computed.\n")


        def k_medoids_clustering():
            if KMedoids is None:
                print("Skipping k-medoids clustering because sklearn_extra is not available.\n")
                return
            print("=== K-Medoids Clustering ===")
            # Generate dataset
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Fit K-Medoids with 2 clusters (since target is binary)
            kmedoids = KMedoids(n_clusters=2, random_state=42)
            clusters = kmedoids.fit_predict(X_scaled)
            score = adjusted_rand_score(y, clusters)
            print(f"Adjusted Rand Index: {score:.2f}\n")


        def k_means_clustering():
            print("=== K-Means Clustering ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kmeans = KMeans(n_clusters=2, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            score = adjusted_rand_score(y, clusters)
            print(f"Adjusted Rand Index: {score:.2f}\n")


        def dbscan_clustering():
            print("=== DBSCAN Clustering ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            dbscan = DBSCAN(eps=0.9, min_samples=5)
            clusters = dbscan.fit_predict(X_scaled)
            # DBSCAN may label some points as noise (-1)
            score = adjusted_rand_score(y, clusters)
            print(f"Adjusted Rand Index: {score:.2f}\n")


        def svm_classifier():
            print("=== SVM Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []

            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = SVC(kernel='linear', random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def random_forest_classifier():
            print("=== Random Forest Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = RandomForestClassifier(random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def loocv():
            print("=== Leave-One-Out Cross-Validation (LOOCV) with SVM ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            loo = LeaveOneOut()
            accuracies = []
            fold = 0
            for train_idx, test_idx in loo.split(X_scaled):
                fold += 1
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = SVC(kernel='linear', random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
            print(f"LOOCV Average Accuracy: {np.mean(accuracies):.2f}\n")


        def k_fold_cv():
            print("=== K-Fold Cross-Validation (Demonstration with SVM) ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = SVC(kernel='linear', random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def grid_search_cv():
            print("=== Grid Search with Cross-Validation (using SVM) ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Parameter grid for SVM
            param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}
            grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=10)
            grid_search.fit(X_scaled, y)
            print("Best Parameters:", grid_search.best_params_)
            print("Best CV Score: {:.2f}\n".format(grid_search.best_score_))


        def pca_analysis():
            print("=== Principal Component Analysis (PCA) ===")
            X, _ = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)
            print("Explained Variance Ratio:", pca.explained_variance_ratio_)
            print("PCA Components shape:", X_pca.shape, "\n")


        def knn_classifier():
            print("=== k-Nearest Neighbors (kNN) Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = KNeighborsClassifier(n_neighbors=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def lda_classifier():
            print("=== Linear Discriminant Analysis (LDA) Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = LinearDiscriminantAnalysis()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def linear_regression_model():
            print("=== Linear Regression Model (rounded predictions for classification) ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = LinearRegression()
                model.fit(X_train, y_train)
                # Round continuous predictions to nearest integer (0 or 1)
                y_pred = np.rint(model.predict(X_test)).astype(int)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def naive_bayes_classifier():
            print("=== Naive Bayes Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = GaussianNB()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        def logistic_regression_model():
            print("=== Logistic Regression Model ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = LogisticRegression(random_state=42, max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")


        if __name__ == "__main__":
            decision_tree_classifier()
            elbow_method()
            k_medoids_clustering()
            k_means_clustering()
            dbscan_clustering()
            svm_classifier()
            random_forest_classifier()
            loocv()
            k_fold_cv()
            grid_search_cv()
            pca_analysis()
            knn_classifier()
            lda_classifier()
            linear_regression_model()
            naive_bayes_classifier()
            logistic_regression_model() 

        def plot_results(X, y, title="Model Results", xlabel="Feature 1", ylabel="Feature 2", class_labels=None):

            General function to plot 2D data points with class labels.

            Parameters:
            - X: 2D numpy array of shape (n_samples, 2), representing the reduced feature space.
            - y: 1D numpy array with class labels (0, 1, 2, etc.).
            - title: Title of the plot.
            - xlabel: Label for the x-axis.
            - ylabel: Label for the y-axis.
            - class_labels: List of class names corresponding to unique values in y.


            # Define colors for different classes
            unique_classes = np.unique(y)
            colors = plt.cm.get_cmap("viridis", len(unique_classes))

            plt.figure(figsize=(8, 6))

            for i, label in enumerate(unique_classes):
                plt.scatter(X[y == label, 0], X[y == label, 1], 
                            color=colors(i), label=class_labels[i] if class_labels else f"Class {label}", alpha=0.7)

            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.legend()
            plt.grid(True)
            plt.show()
        """)

def custom_import():
     print( """
        import numpy as np
        from sklearn.datasets import make_classification
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import KFold, LeaveOneOut, GridSearchCV
        from sklearn.metrics import accuracy_score, adjusted_rand_score
        from sklearn.linear_model import LinearRegression, LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.svm import SVC
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.naive_bayes import GaussianNB
        from sklearn.cluster import KMeans, DBSCAN
        from sklearn.decomposition import PCA
        """)
def decision_tree_classifier():
    print("""
        print("=== Decision Tree Classifier ===")
            # Generate synthetic dataset
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # 10-fold cross-validation
            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            fold_accuracies = []

            for fold, (train_index, test_index) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_index], X_scaled[test_index]
                y_train, y_test = y[train_index], y[test_index]

                model = DecisionTreeClassifier(max_depth=3, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                fold_accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")

            print(f"Average Accuracy: {np.mean(fold_accuracies):.2f}\n")
        """)
def elbow_method():
    print("""
        print("=== Elbow Method (using KMeans inertia) ===")
            # Use only features from synthetic data (ignore labels)
            X, _ = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            inertias = {}
            for k in range(1, 11):
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(X_scaled)
                inertias[k] = kmeans.inertia_
                print(f"k = {k}, Inertia = {kmeans.inertia_:.2f}")
            print("Elbow method values computed.\n")
        """)

def k_medoids_clustering():
    print("""
        if KMedoids is None:
                    print("Skipping k-medoids clustering because sklearn_extra is not available.\n")
                    return
                print("=== K-Medoids Clustering ===")
                # Generate dataset
                X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                        n_redundant=0, n_classes=2, random_state=42)
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                # Fit K-Medoids with 2 clusters (since target is binary)
                kmedoids = KMedoids(n_clusters=2, random_state=42)
                clusters = kmedoids.fit_predict(X_scaled)
                score = adjusted_rand_score(y, clusters)
                print(f"Adjusted Rand Index: {score:.2f}\n")
        """)

def k_means_clustering():
    print("""
        print("=== K-Means Clustering ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kmeans = KMeans(n_clusters=2, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            score = adjusted_rand_score(y, clusters)
            print(f"Adjusted Rand Index: {score:.2f}\n")
        """)

def dbscan_clustering():
    print("""
     print("=== DBSCAN Clustering ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            dbscan = DBSCAN(eps=0.9, min_samples=5)
            clusters = dbscan.fit_predict(X_scaled)
            # DBSCAN may label some points as noise (-1)
            score = adjusted_rand_score(y, clusters)
            print(f"Adjusted Rand Index: {score:.2f}\n")
    """)

def svm_classifier():
    print(
        """
        print("=== SVM Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []

            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = SVC(kernel='linear', random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )

def random_forest_classifier():
    print(
        """
         print("=== Random Forest Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = RandomForestClassifier(random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def loocv():
    print(
        """
        print("=== Leave-One-Out Cross-Validation (LOOCV) with SVM ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            loo = LeaveOneOut()
            accuracies = []
            fold = 0
            for train_idx, test_idx in loo.split(X_scaled):
                fold += 1
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = SVC(kernel='linear', random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
            print(f"LOOCV Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def k_fold_cv():
    print(
        """
         print("=== K-Fold Cross-Validation (Demonstration with SVM) ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = SVC(kernel='linear', random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def grid_search_cv():
    print(
        """
        print("=== Grid Search with Cross-Validation (using SVM) ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Parameter grid for SVM
            param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}
            grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=10)
            grid_search.fit(X_scaled, y)
            print("Best Parameters:", grid_search.best_params_)
            print("Best CV Score: {:.2f}\n".format(grid_search.best_score_))
        """
    )
def pca_analysis():
    print(
        """
         print("=== Principal Component Analysis (PCA) ===")
            X, _ = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)
            print("Explained Variance Ratio:", pca.explained_variance_ratio_)
            print("PCA Components shape:", X_pca.shape, "\n")
        """
    )
def knn_classifier():
    print(
        """
         print("=== k-Nearest Neighbors (kNN) Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = KNeighborsClassifier(n_neighbors=5)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")

        """
    )
def lda_classifier():
    print(
        """
         print("=== Linear Discriminant Analysis (LDA) Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = LinearDiscriminantAnalysis()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def linear_regression_model():
    print(
        """
         print("=== Linear Regression Model (rounded predictions for classification) ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = LinearRegression()
                model.fit(X_train, y_train)
                # Round continuous predictions to nearest integer (0 or 1)
                y_pred = np.rint(model.predict(X_test)).astype(int)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def naive_bayes_classifier():
    print(
        """
         print("=== Naive Bayes Classifier ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = GaussianNB()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def logistic_regression_model():
    print(
        """
        print("=== Logistic Regression Model ===")
            X, y = make_classification(n_samples=100, n_features=20, n_informative=5,
                                    n_redundant=0, n_classes=2, random_state=42)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kf = KFold(n_splits=10, shuffle=True, random_state=42)
            accuracies = []
            for fold, (train_idx, test_idx) in enumerate(kf.split(X_scaled), 1):
                X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                model = LogisticRegression(random_state=42, max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                accuracies.append(acc)
                print(f"Fold {fold} Accuracy: {acc:.2f}")
            print(f"Average Accuracy: {np.mean(accuracies):.2f}\n")
        """
    )
def plot():
    print(
        """
        def plot_results(X, y, title="Model Results", xlabel="Feature 1", ylabel="Feature 2", class_labels=None):

            General function to plot 2D data points with class labels.

            Parameters:
            - X: 2D numpy array of shape (n_samples, 2), representing the reduced feature space.
            - y: 1D numpy array with class labels (0, 1, 2, etc.).
            - title: Title of the plot.
            - xlabel: Label for the x-axis.
            - ylabel: Label for the y-axis.
            - class_labels: List of class names corresponding to unique values in y.


            # Define colors for different classes
            unique_classes = np.unique(y)
            colors = plt.cm.get_cmap("viridis", len(unique_classes))

            plt.figure(figsize=(8, 6))

            for i, label in enumerate(unique_classes):
                plt.scatter(X[y == label, 0], X[y == label, 1], 
                            color=colors(i), label=class_labels[i] if class_labels else f"Class {label}", alpha=0.7)

            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.legend()
            plt.grid(True)
            plt.show()
        """
    )
def weare():
    print(
        """
        custom_sklearn()
        custom_import()
        decision_tree_classifier()
        elbow_method()
        k_medoids_clustering()
        k_means_clustering()
        dbscan_clustering()
        svm_classifier()
        random_forest_classifier()
        loocv()
        k_fold_cv()
        grid_search_cv()
        pca_analysis()
        knn_classifier()
        lda_classifier()
        linear_regression_model()
        naive_bayes_classifier()
        logistic_regression_model()
        plot()
        """
    )
