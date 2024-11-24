from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from utils.utilities import load_image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def kmeans_3d(image_path, k):
    # 이미지 로드
    image, image_shape = load_image(image_path)

    # 이미지를 2D 배열로 변환
    pixels = image.reshape(-1, 3)

    # 클러스터링 수행
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)

    labels = kmeans.labels_
    new_colors = kmeans.cluster_centers_.astype(np.uint8)

    # 처리된 이미지 처리
    compressed_image = new_colors[labels].reshape(image_shape)
    return compressed_image, labels, new_colors


def kmeans_5d(image_path, k, spatial_weight):
    # load image
    image, image_shape = load_image(image_path)

    data_5d = get_5d_data(image, spatial_weight)

    # 클러스터링 수행
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_5d)
    labels = kmeans.labels_
    new_colors = kmeans.cluster_centers_[:, :3].astype(np.uint8)    # RGB부분만 사용

    # 이미지 처리
    compressed_image = new_colors[labels].reshape(image_shape)
    return compressed_image, labels, new_colors


def visualize_3d_rgb(image, output_path, title: str,
                     labels=None, center_colors=None,
                     max_width=400, max_height=400):
    pixels = image.reshape(-1, 3)   # 2D 벡터화

    # for clustered image
    if labels is not None and center_colors is not None:
        print("clustered")
        colors_to_plot = center_colors[labels] / 255.0
    else:
        colors_to_plot = pixels / 255.0

    r, g, b = pixels[:, 0], pixels[:, 1], pixels[:, 2]  # RGB 채널 분리

    # 그래프 크기 조정
    aspect_ratio = max_width / max_height
    figsize = (aspect_ratio * 5, 5)     # 기본적으로 높이를 기준으로 조정

    # 3D 시각화
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(r, g, b, c=colors_to_plot, marker='o', s=1)
    ax.set_xlabel("Red Channel")
    ax.set_ylabel("Green Channel")
    ax.set_zlabel("Blue Channel")
    ax.set_title(title)

    # save visualize graph
    plt.savefig(output_path)
    plt.close(fig)


def visualize_5d_pca(data_5d, output_path, title: str, max_width=400, max_height=400):
    # PCA를 사용하여 3D로 축소
    pca = PCA(n_components=3)
    reduced_data = pca.fit_transform(data_5d)

    # 3D 데이터 분리
    r, g, b = reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2]

    # 그래프 크기 조정
    aspect_ratio = max_width / max_height
    figsize = (aspect_ratio * 5, 5)

    # 3D 시각화
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(r, g, b, c=data_5d[:, :3]/255, marker='o', s=1)      # RGB 기반으로 색상 설정
    ax.set_xlabel("PCA1")
    ax.set_ylabel("PCA2")
    ax.set_zlabel("PCA3")
    ax.set_title(title)

    # 그래프 저장
    plt.savefig(output_path)
    plt.close(fig)


def get_5d_data(image, spatial_weight):
    # RGB 값과 픽셀 좌표(x, y)를 포함한 5D 데이터 생성
    rows, cols, dims = image.shape
    pixels = image.reshape(-1, 3)
    x_coords = np.repeat(np.arange(rows), cols)[:, np.newaxis]  # 행 좌표
    y_coords = np.tile(np.arange(cols), rows)[:, np.newaxis]  # 열 좌표

    # 5D 데이터 (RGB + x, y) 생성
    return np.hstack((pixels, spatial_weight * x_coords, spatial_weight * y_coords))