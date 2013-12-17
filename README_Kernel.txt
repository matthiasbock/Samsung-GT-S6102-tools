HOW TO BUILD KERNEL 2.6.35.7 FOR GT-S6102

1. How to Build
	- download Linux kernel sources from http://www.kernel.org/
	- get a toolchain
		e.g. visit http://www.codesourcery.com/, download and install Sourcery G++ Lite 2009q3-68 toolchain for ARM EABI
		or use the GNU ARM EABI from The Embedded Debian Project (http://www.emdebian.org/)
	- extract kernel source
	- download bcm21553_torino_02_defconfig and save it as as .config within the top directory of the kernel source tree
	$ make

2. Output files
	- Kernel : kernel/common/arch/arm/boot/zImage
	
3. How to make .tar binary for downloading into target.
	- change current directory to kernel/common/arch/arm/boot
	- type following command
	$ tar cvf GT-S6102_Kernel_Gingerbread.tar zImage
