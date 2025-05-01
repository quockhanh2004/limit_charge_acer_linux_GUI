pkgname=acer-battery-control-gui
pkgver=1.1.3
pkgrel=1
pkgdesc="A simple GUI to control Acer battery health mode."
arch=("any")
url="https://your.project.url"
license=("MIT")
depends=("python3" "python-pyqt5" "base-devel" "linux-headers")
makedepends=("python")
provides=("acer-battery-manager")
conflicts=("acer-battery-manager-other")
install="${pkgname}.install"

source=(
    "gui.py"
    "backend.py"
    "acer-battery-control-gui.service"
    "acer-battery-control.rules"
    "acer-wmi-battery.c"
    "Makefile"
    "acer-battery-health.desktop"
    "acer-care-center_48x48.png"
    "acer-care-center_256x256.png"
    "LICENSE"
    "README.md"
)

md5sums=('47faf4a607a8a97e4633254159703223'
         'ab1a797b8b0e8d45ecff589c8b005c81'
         'f96c4057cf13978318760a4a882af1e6'
         '04f9aa5b03321da2fa1937392cfb9020'
         'd67cc8f9cd9f6de96465a2a391d8672e'
         '2afe5e9249a1ee421b0a165deb84260e'
         '377c5f4ef1218dec09967bfea74fa3b2'
         '271fb148077017e87d114f000c9f5ce4'
         '268602bfba61e6ee16de750be4a0469b'
         'b234ee4d69f5fce4486a80fdaf4a4263'
         '4983ceab2e98c9affb6d2e3768d6ea49')

package() {
  # 1. Cài app GUI
  install -Dm755 gui.py "${pkgdir}/usr/bin/acer-battery-control-gui"
  install -Dm755 backend.py "${pkgdir}/etc/acer-battery-control-gui/backend.py"
  install -Dm644 acer-battery-control.rules "${pkgdir}/usr/share/polkit-1/rules.d/acer-battery-control.rules"
  install -Dm644 acer-battery-control-gui.service "${pkgdir}/usr/lib/systemd/system/acer-battery-control-gui.service"
  install -Dm644 acer-battery-health.desktop "${pkgdir}/usr/share/applications/acer-battery-health.desktop"
  install -Dm644 acer-care-center_256x256.png "${pkgdir}/usr/share/icons/hicolor/256x256/apps/acer-battery-control.png"
  install -Dm644 acer-care-center_48x48.png "${pkgdir}/usr/share/icons/hicolor/48x48/apps/acer-battery-control.png"
  install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
  install -Dm644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"

  # 2. Build kernel module
  _kernver=$(uname -r)
  mkdir -p "${srcdir}/buildmod"
  cp acer-wmi-battery.c Makefile "${srcdir}/buildmod/"
  make -C /lib/modules/"${_kernver}"/build M="${srcdir}/buildmod" modules

  # 3. Copy module đã build vào package
  install -Dm644 "${srcdir}/buildmod/acer-wmi-battery.ko" \
    "${pkgdir}/usr/lib/modules/${_kernver}/extra/acer-wmi-battery.ko"
}

