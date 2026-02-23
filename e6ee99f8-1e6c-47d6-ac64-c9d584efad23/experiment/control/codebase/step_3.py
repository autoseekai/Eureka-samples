import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

BASE_DIR = '/work_dir'
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOT_DIR = os.path.join(BASE_DIR, 'plots')
INVESTOR_FILE = os.path.join(DATA_DIR, 'investors.csv')
CASH_FLOW_FILE = os.path.join(DATA_DIR, 'cash_flows.csv')
MAX_CLUSTERS = 10
OPTIMAL_CLUSTERS = 4

def generate_plot_filename(name, number):
    """
    Generates a filename for a plot with a timestamp.

    Args:
        name (str): The base name for the plot.
        number (int): The plot number.

    Returns:
        str: A formatted filename string.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = '%s_%d_%s.png' % (name, number, timestamp)
    return os.path.join(PLOT_DIR, filename)

def load_data(investor_path, cash_flow_path):
    """
    Loads investor and cash flow data from CSV files.

    Args:
        investor_path (str): The file path for the investor data.
        cash_flow_path (str): The file path for the cash flow data.

    Returns:
        tuple: A tuple containing two pandas DataFrames (investors, cash_flows).
    """
    investors_df = pd.read_csv(investor_path)
    cash_flows_df = pd.read_csv(cash_flow_path)
    return investors_df, cash_flows_df

def engineer_features(investors_df, cash_flows_df):
    """
    Engineers features for clustering from investor and cash flow data.

    This function calculates transaction frequency for each investor and combines
    it with AUM and risk profile. The 'risk_profile' column is assumed to be
    ordinal and is mapped to numerical values.

    Args:
        investors_df (pd.DataFrame): DataFrame with investor data.
        cash_flows_df (pd.DataFrame): DataFrame with cash flow data.

    Returns:
        pd.DataFrame: A DataFrame with engineered features for each investor.
    """
    transaction_counts = cash_flows_df['investor_id'].value_counts().reset_index()
    transaction_counts.columns = ['investor_id', 'transaction_frequency']

    features_df = pd.merge(investors_df, transaction_counts, on='investor_id', how='left')
    features_df['transaction_frequency'] = features_df['transaction_frequency'].fillna(0)

    risk_profile_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    features_df['risk_profile_encoded'] = features_df['risk_profile'].map(risk_profile_mapping)

    feature_columns = ['initial_aum', 'risk_profile_encoded', 'transaction_frequency']
    final_features = features_df[['investor_id'] + feature_columns].set_index('investor_id')

    return final_features

def scale_features(features_df):
    """
    Scales the features using StandardScaler.

    Args:
        features_df (pd.DataFrame): DataFrame of features to be scaled.

    Returns:
        np.ndarray: A NumPy array of the scaled features.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features_df)
    return scaled_data

def plot_elbow_method(scaled_data, max_k, file_path):
    """
    Calculates and plots the inertia for a range of k values (Elbow Method).

    This helps in determining the optimal number of clusters for K-Means.

    Args:
        scaled_data (np.ndarray): The scaled feature data.
        max_k (int): The maximum number of clusters to test.
        file_path (str): The path to save the output plot.
    """
    inertia = []
    k_range = range(1, max_k + 1)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_data)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertia, marker='o', linestyle='--')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia (Within-Cluster Sum of Squares)')
    plt.title('Elbow Method for Optimal k')
    plt.xticks(k_range)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(file_path, dpi=300)
    plt.close()
    print('Plot saved to: ' + file_path)

def perform_clustering(scaled_data, n_clusters):
    """
    Performs K-Means clustering on the data.

    Args:
        scaled_data (np.ndarray): The scaled feature data.
        n_clusters (int): The number of clusters to form.

    Returns:
        np.ndarray: An array of cluster labels for each data point.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled_data)
    return labels

def reduce_dimensions_with_pca(scaled_data):
    """
    Reduces the data to two principal components using PCA.

    Args:
        scaled_data (np.ndarray): The scaled feature data.

    Returns:
        pd.DataFrame: A DataFrame with the first two principal components.
    """
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_data)
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    return pca_df

def plot_clusters(pca_df, labels, file_path):
    """
    Creates and saves a scatter plot of the clustered data.

    The plot shows the first two principal components, with points colored
    by their assigned cluster.

    Args:
        pca_df (pd.DataFrame): DataFrame with principal components.
        labels (np.ndarray): Array of cluster labels.
        file_path (str): The path to save the output plot.
    """
    plt.figure(figsize=(12, 8))
    unique_labels = np.unique(labels)
    scatter = plt.scatter(pca_df['PC1'], pca_df['PC2'], c=labels, cmap='viridis', alpha=0.7)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Customer Segments via K-Means Clustering (PCA)')
    plt.grid(True)

    legend_elements = scatter.legend_elements()
    cluster_names = ['Cluster ' + str(i) for i in unique_labels]
    plt.legend(legend_elements[0], cluster_names, title="Segments")

    plt.tight_layout()
    plt.savefig(file_path, dpi=300)
    plt.close()
    print('Plot saved to: ' + file_path)

if __name__ == '__main__':
    """
    Main execution block for Step 3: Customer Segmentation and Visualization.

    This script performs the following actions:
    1. Creates the output directory for plots if it does not exist.
    2. Loads investor and cash flow data.
    3. Engineers features for clustering (AUM, risk profile, transaction frequency).
    4. Scales the features to prepare them for K-Means.
    5. Generates and saves an 'Elbow Method' plot to help determine the optimal k.
    6. Performs K-Means clustering with a predefined optimal number of clusters.
    7. Uses PCA to reduce feature dimensions for visualization.
    8. Generates and saves a scatter plot of the customer segments.
    """
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)

    investors, cash_flows = load_data(INVESTOR_FILE, CASH_FLOW_FILE)

    features = engineer_features(investors, cash_flows)

    scaled_features = scale_features(features)

    elbow_plot_path = generate_plot_filename('elbow_method', 1)
    plot_elbow_method(scaled_features, MAX_CLUSTERS, elbow_plot_path)

    cluster_labels = perform_clustering(scaled_features, OPTIMAL_CLUSTERS)

    pca_result_df = reduce_dimensions_with_pca(scaled_features)

    cluster_plot_path = generate_plot_filename('customer_segments', 2)
    plot_clusters(pca_result_df, cluster_labels, cluster_plot_path)
