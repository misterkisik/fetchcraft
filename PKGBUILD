# Maintainer: misterkisik
pkgname=fetchcraft
pkgver=1.0.0
pkgrel=1
pkgdesc="Interactive Visual GUI Configurator and Live Terminal Designer for Fastfetch"
arch=('any')
url="https://github.com/misterkisik/fetchcraft"
license=('GPL-3.0-or-later')
depends=(
    'fastfetch'
    'gtk4'
    'libadwaita'
    'python'
    'python-gobject'
    'vte4'
)
makedepends=(
    'python-build'
    'python-installer'
    'python-setuptools'
    'python-wheel'
)
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 data/org.cleanarch.FetchCraft.desktop "$pkgdir/usr/share/applications/org.cleanarch.FetchCraft.desktop"
    install -Dm644 data/icons/hicolor/scalable/apps/org.cleanarch.FetchCraft.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/org.cleanarch.FetchCraft.svg"
}
