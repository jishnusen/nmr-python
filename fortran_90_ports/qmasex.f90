!--------------------------------------------------------------
!     exchange between all sites in two quadrupolar broadened
!     lineshapes under MAS condition for central transition only
!--------------------------------------------------------------
    subroutine qmasex(f,g,sqn,vlf,eta1,eqqh1,cs1,t2one,npolar1,nazim1,eta2,eqqh2,cs2,t2two,npolar2,nazim2,hi,lo,jfreq)
    dimension freq1(1000000),freq2(1000000),g(1000)
    dimension f(1000)
    !f2py intent(out) f
    !f2py intent(out) g
    common pi
    complex :: l
    real :: sqn
    real :: vlf
    real :: eta1
    real :: eqqh1
    real :: cs1
    real :: t2one
    integer :: npolar1
    integer :: nazim1
    real :: eta2
    real :: eqqh2
    real :: cs2
    real :: t2two
    integer :: npolar2
    integer :: nazim2
    real :: hi
    real :: lo
    real :: jfreq
    npts=1000
    pi=3.1415927
    cs1=cs1*vlf
    cs2=cs2*vlf
!----------------------------------------------------------------
!     generate frequencies for all the sites
!-------------------------------------------------
    call quadfreq(npolar1,nazim1,cs1,eta1,eqqh1,freq1,vlf,sqn)
    call quadfreq(npolar2,nazim2,cs2,eta2,eqqh2,freq2,vlf,sqn)
    nfreq1=npolar1*nazim1
    nfreq2=npolar2*nazim2
    do 30 i=1,nfreq2
    !----------------------------------------------------
    !     put frequencies in one array
    !---------------------------------------------
        freq1(i+nfreq1)=freq2(i)
        continue
    30 END DO
    nfreq=nfreq1+nfreq2
    jfreq=jfreq/float(nfreq-1)
    ar1=float(nfreq)*jfreq+1.0/t2one
    ar2=float(nfreq)*jfreq+1.0/t2two
    hi=hi*vlf
    lo=lo*vlf
    dwf=(hi-lo)/float(npts-1)
    gmax=0.0
!--------------------------------------------------------
!     do lineshape calculation a la Mehring pg 61
!---------------------------------------------------------
    do 300 i=1,npts
        wf=lo+dwf*float(i-1)
        l=(0.0,0.0)
        do 400 j=1,nfreq1
            l=l+cmplx(1.0,0.0)/cmplx(ar1,wf-freq1(j))
            continue
        400 END DO
        nfr=nfreq1+1
        do 410 j=nfr,nfreq
            l=l+cmplx(1.0,0.0)/cmplx(ar2,wf-freq1(j))
            continue
        410 END DO
        g(i)=real(l/(cmplx(1.0,0.0)-(cmplx(jfreq,0.0)*l)))
        g(i)=g(i)/float(nfreq)
        if(g(i) > gmax) gmax=g(i)
        continue
    300 END DO
!--------------------------------------------------------
!     normalise
!------------------------------------------------------
    do 500 i=1,npts
        wf=lo+float(i-1)*dwf
        wf=wf/vlf
        g(i)=g(i)/gmax
        f(i)=wf
        continue
    500 END DO
    end
!
!******************************************************************
!	The following subroutine calculates quadrupolar MAS 
!	powder patterns for central transitions
!******************************************************************
    subroutine quadfreq(npolar,nazim,cs,eta,eqqh,freq,vlf,sqn)
    dimension freq(100000)
    common pi
    dpolar=2.0/float(npolar-1)
    dazim=pi/float(nazim-1)
    vq=(3.0*eqqh*1.0e6)/(2.0*sqn*(2.0*sqn-1.0))
    f=(sqn*(sqn+1.0))-0.75
    f=f*vq*vq/(6.0*vlf*1.0e6)
    k=0
    do 100 i=1,npolar
        ct=-1.0+dpolar*float(i-1)
        ct2=ct*ct
        do 200 j=1,nazim
            k=k+1
            phi=dazim*float(j-1)
            c2phi=cos(2.0*phi)
            aphi=1.3125-(0.875*eta*c2phi)+(.1458*eta*eta*c2phi*c2phi)
            bphi=-1.125+((eta*eta)/12)+(eta*c2phi)-(.2917*eta*eta*c2phi*c2phi)
            cphi=0.3125-(.125*eta*c2phi)+(0.1458*eta*eta*c2phi*c2phi)
            v=-((aphi*ct2*ct2)+(bphi*ct2)+cphi)
            freq(k)=(v*f)+cs
            continue
        200 END DO
        continue
    100 END DO
    return
    end
