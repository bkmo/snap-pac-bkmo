# Maintainer: NicoHood <archlinux {cat} nicohood {dog} de>
# PGP ID: 97312D5EB9D7AE7D0BD4307351DAE9B7C1AE9161
# Contributor: Wes Barnett <wes at wbarnett dot us>

pkgname=snap-pac-bkmo
pkgver=3.0.1.1
pkgrel=1
pkgdesc="Pacman hooks that use snapper to create pre/post btrfs snapshots like openSUSE's YaST"
arch=('any')
url="https://github.com/bkmo/snap-pac-bkmo"
license=('GPL')
depends=('snapper' 'pacman' 'btrfs-progs' 'procps-ng' 'python')
makedepends=('git' 'python-sphinx')
provides=('snap-pac')
conflicts=('snap-pac')
replaces=('snap-pac')
backup=('etc/snap-pac.ini')

source=("https://github.com/bkmo/snap-pac-bkmo/archive/refs/tags/3.0.1.1.tar.gz")
md5sums=('SKIP')

package() {
  cd $pkgname-$pkgver
  make DESTDIR="$pkgdir/" install
}
