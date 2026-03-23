case $(uname -n) in
    openbook-arch)
        export AQ_DRM_DEVICES=/dev/dri/nvidia-dgpu:/dev/dri/intel-igpu
        ;;
    bennequin-arch)
        export AQ_DRM_DEVICES=/dev/dri/intel-igpu
        ;;
    *)
        export AQ_DRM_DEVICES=
        ;;
esac
