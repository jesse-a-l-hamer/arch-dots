case $(uname -n) in
openbook-arch)
    export GBM_BACKEND=nvidia-drm
    export __GLX_VENDOR_LIBRARY_NAME=nvidia
    export LIBVA_DRIVER_NAME=nvidia
    export NVD_BACKEND=direct
    export ELECTRON_OZONE_PLATFORM_HINT=auto
    export MOZ_DISABLE_RDD_SANDBOX=1
    ;;
bennequin-arch) ;;
*) ;;
esac
