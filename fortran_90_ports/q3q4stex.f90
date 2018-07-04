!     file: q3q4stex.f
    subroutine q3q4stex(f,g,vlf,avspara,avsperp,ncth,jfreq,t2,fu,fl,posq4)
    dimension f(1000),w(61000),g(1000),q4int(5000)
!f2py intent(out) f
!f2py intent(out) g
    dimension pq4(1000),gnsperp(50),sperp(50),spara(50)
    complex :: l
    real :: vlf
    real :: avspara
    real :: avsperp
    integer :: ncth
    real :: jfreq
    real :: t2
    real :: fu
    real :: fl
    real :: posq4
    pi=3.141927

    nf=1000

!     Larmor frequency is 79.459 MHz (29Si)

!     read(5,10)infile
!     open(9,file=infile,status='old')
    f0=vlf
    w0=2.0*pi*f0
!      write(6,20)
! 0    format('enter sigma parallel, sigma perp. (ppm):')
!      read(5,*)avspara,avsperp
!      write(6,30)
! 0    format('enter number of sites (cos thetas):')
!      read(5,*)ncth
!     open(8,file='param')
!     read(8,20)outfile
! 0    format(a20)
!      read(8,*)ncth,jfreq,t2
! 5    format(i5,f12.2,f6.4)
!      close(8)
    dcth=2.0/float(ncth-1)
!      write(6,40)
! 0    format('enter upper and lower limits of spectrum (ppm):')
!      read(5,*)fu,fl
    wfu=fu*w0
    wfl=fl*w0
!      write(6,50)
! 0    format('enter number of freq. divisions:')
!      read(5,*)nf
    dwf=(wfu-wfl)/float(nf-1)
    df=(fu-fl)/float(nf-1)
    do 55 i=1,nf
        f(i)=fl+df*float(i-1)
    55 END DO
!      write(6,500)
! 00   format('enter Q4 position (ppm), width (fwhm):')
!      read(5,*)posq4,width
    width=22.0

!     create gaussian distribution of q4 occurences

    deltaq4=(2.0*width/160.0)
    width=width/2.354
    width=1.0/width
    sum=0.0
    do 1000 i=1,161
        gb=0.0
        pq4(i)=posq4-deltaq4*float(81-i)
        gb=(pq4(i)-posq4)*width
        gb=(gb*gb)/2.0
        gb=width*0.3989*exp(-gb)
        q4int(i)=gb
        sum=sum+q4int(i)
    1000 END DO
    do 2000 i=1,161
        q4int(i)=q4int(i)*float(ncth)/sum
    2000 END DO

!     assign q4 frequencies according to gaussian distribution

    k=1
    m=0
    do 3000 i=1,161
        m=m+nint(q4int(i))
        do 4000 j=k,m
            w(ncth+j)=pq4(i)*w0
        4000 END DO
        k=1+m
    3000 END DO



!      write(6,60)
! 0    format('enter jump freq. (Hz) + T2 (s):')
!      read(5,*)jfreq,t2

    jfreq=jfreq/(float(2*ncth)-1.0)
    ar=float(2*ncth)*jfreq+1.0/t2

!     create gaussian distribution of q3 parameters

    sum=0.0
    gwidth=20.0
    deltagw=1.5*gwidth/40.0
    gwidth=1.0/(gwidth/2.354)
    do 200 i=1,31
        sperp(i)=avsperp-float(21-i)*deltagw
        spara(i)=avspara-float(21-i)*deltagw
        gb=0.0
        gb=(sperp(i)-avsperp)*gwidth
        gb=(gb*gb)/2.0
        gb=gwidth*0.3989*exp(-gb)
        gnsperp(i)=gb
        sum=sum+gb
    200 END DO
    do 300 i=1,41
        gnsperp(i)=gnsperp(i)*(float(ncth)/sum)
    300 END DO

!     calculate q3 frequencies for gaussian distribution

    ik=1
    im=0
    do 75 k=1,41
        ng=nint(gnsperp(k))
        im=im+ng
        dcth=2.0/float(ng-1)
        wperp=sperp(k)*w0
        wpara=spara(k)*w0
        do 80 i=ik,im
            ii=i-ik+1
            cth=1.0-dcth*(float(ii-1))
            csqth=cth*cth
            ssqth=1.0-csqth
            w(i)=wperp*ssqth+wpara*csqth
        80 END DO
        ik=im+1
    75 END DO

!     start lineshape calculation

    ncth=2*ncth
    do 90 j=1,nf
        wf=wfl+dwf*float(j-1)
        l=(0.0,0.0)
        do 100 k=1,ncth
            l=l+cmplx(1.0,0.0)/cmplx(ar,wf-w(k))
        100 END DO
        g(j)=real(l/(cmplx(1.0,0.0)-(cmplx(jfreq,0.0)*l)))
        g(j)=g(j)/float(ncth)
    90 END DO

!     normalise and write to file

    rmax=0.0
    do 110 i=1,nf
        if(g(i) > rmax) rmax=g(i)
    110 END DO
!     open(7,file=outfile)
    do 120 i=1,nf
        ppm=fl+df*float(i-1)
        g(i)=g(i)/rmax
        f(i)=ppm
    120 END DO
    end
