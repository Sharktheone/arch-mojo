pkgname=modular
pkgver=0.5.1
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
sha256sums=("9747968d724afad372916eb6113c0c1cfa5d5a1ca5806cba44f73f89fc703d20")

package() {
    bsdtar -xf data.tar -C "$pkgdir/"
}
