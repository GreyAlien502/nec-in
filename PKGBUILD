# An example PKGBUILD script for Civetweb upstream, git version
# Rename to PKGBUILD to build via makepkg
_pkgname=nec-in
pkgname=$_pkgname-git
pkgver=1759378017
pkgrel=1
pkgdesc="minimal monospace font"
arch=('any')
url="https://www.github.com/GreyAlien502/nec-in"
license=('GPL')
groups=()
depends=()
makedepends=(fontforge ttf-unifont bdf2psf psftools)
optdepends=('brotli: for smaller woff2 file', 'python-fonttools: must be installed by pacman or pip','python-bdf2ttf: must be installed from pip')
provides=("$_pkgname")
conflicts=("$_pkgname")
backup=("etc/$_pkgname/$_pkgname.conf")
source=("$_pkgname::git+https://github.com/GreyAlien502/$_pkgname.git")
md5sums=('SKIP')

pkgver() {
	cd "$srcdir/$_pkgname"
	git show -s --format=%ct
}

build() {
	cd "$srcdir/$_pkgname"
	make
}

package() {
	target_dir="/usr/share/$_pkgname/"

	while read ext dir
		do
			install -dm755 "$pkgdir/$dir"
			install -Dm644 -t "$pkgdir/$dir" "$srcdir/$_pkgname/build/"nec-in."$ext"
		done <<-DD
			ttf	/usr/share/fonts/$_pkgname/
			psf.gz	/usr/share/kbd/consolefonts/
			pf2	/usr/share/grub/
			flf	/usr/share/figlet/
			woff2	$target_dir
			bdf	$target_dir
		DD
}
