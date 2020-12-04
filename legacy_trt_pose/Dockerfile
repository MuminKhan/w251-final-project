FROM nvcr.io/nvidia/l4t-pytorch:r32.4.4-pth1.6-py3

ARG MODEL_WEIGHTS=https://drive.google.com/u/0/uc?id=1XYDdCUdiF2xxx4rznmLb62SdOUZuoNbd
ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV INSTALL_DIR=/final

WORKDIR ${INSTALL_DIR}

RUN apt update &&   \
    apt install -y  \
        jupyter     \
        python3-matplotlib && \
    apt clean &&    \
    pip3 install    \
        cython          \
        gdown           \
        ipywidgets      \
        pycocotools     \
        tqdm         && \
    jupyter nbextension enable --py widgetsnbextension && \
    cd ${INSTALL_DIR} && \
    git clone https://github.com/NVIDIA-AI-IOT/torch2trt && cd torch2trt && \ 
        python3 setup.py install --plugins && \
    cd ${INSTALL_DIR} && \
    git clone https://github.com/NVIDIA-AI-IOT/trt_pose && cd trt_pose && \
        python3 setup.py install && \
    cd tasks/human_pose && \
    gdown ${MODEL_WEIGHTS}

WORKDIR ${INSTALL_DIR}/trt_pose/tasks/human_pose

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]