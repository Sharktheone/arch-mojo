pkgname=modular
pkgver=0.2.0
pkgrel=1
pkgdesc="Modular installation tool"
url="https://developer.modular.com/download"
license=("custom:modular")
depends=(
    "python"
    "python-pip"
    "ncurses"
    "libxml2"
)
arch=("x86_64")
source=("https://dl.modular.com/public/installer/deb/debian/pool/any-version/main/m/mo/modular_$pkgver/modular-$pkgver-amd64.deb")
sha256sums=("7b958ac02260ae9a7224c6ae50860a4dd00089ffc00fc87a0c56585b34c10849")

package() {
    bsdtar -xf data.tar -C "$pkgdir/"
}