!------------------------------------------------------------------------
!
!        bcsax is a chemical exchange lineshape simulation program
!       for one site with a general CSA powder pattern based on
!       a model of random tumbling of the molecules with orientational
!       exchange between all possible orientations with a single time
!       constant. This program analytically inverts the exchange matrix
!       For details see Mehring's book, p. 61.
!
!------------------------------------------------------------------------
    subroutine bcsax(f,g,s11,s22,s33,jfreq,t2,fu,fl,w0)
    dimension tint(500000)
    dimension g(1000)
    dimension f(1000)
    !f2py intent(out) f
    !f2py intent(out) g
    dimension w(500000)
    complex :: l
    real :: s11,s22,s33,jfreq,t2
    integer fu,fl,smo
    pi=22.0/7.0
    smo=1
    nt=5000
!-----------------------------------------------------------------------
!	Reading input parameters interactively
!-----------------------------------------------------------------------
!**********These are chemical shifts from the powder pattern**********
    wfu=fu*w0
    wfl=fl*w0
    nsite=(fu-fl)*10
    nf=1000
    dwf=(wfu-wfl)/float(nf-1)
    df=(fu-fl)/float(nf-1)
    do 55 i=1,nf
        f(i)=fl+df*float(i-1)
        continue
    55 END DO
!----------------------------------------------------------------------
!     calculate frequencies and intensities for the lineshape
!----------------------------------------------------------------------
    wsig11=s11*w0
    wsig22=s22*w0
    wsig33=s33*w0
!*********************
    do 200 i=1,nsite
        tint(i)=0
        continue
    200 END DO
    do 501 i=1,nsite
        w(i)=0
        continue
    501 END DO
    sum=0.0
    dif1=s33-s11
    dif2=s33-s22
    dif3=s22-s11
    is=nint(s11-fl)+1
    ib=nint(s22-fl)+1
    it=nint(s33-fl)+1
    ibm1=ib-1
    a0=1.3862944
    a1=0.1119723
    b0=0.50
    a2=0.0725296
    b1=0.1213478
    b2=0.0288729
    do 201 k=is,ibm1
        pm=sqrt(dif1*dif2/((it-k)*dif3))
        par=(k-is)*dif2/((it-k)*dif3)
        v=1.0-par
        eint=a0+a1*v+a2*v**2+(b0+b1*v+b2*v**2)*alog(1.0/v)
        tint(k)=pm*eint
        sum=sum+(tint(k))
        continue
    201 END DO
    ibp1=ib+1
    do 202 k=ibp1,it
        pm=sqrt(dif1/(k-is))
        par=dif3*(it-k)/(dif2*(k-is))
        v=1.0-par
        eint=a0+a1*v+a2*v**2+(b0+b1*v+b2*v**2)*alog(1.0/v)
        tint(k)=pm*eint
        sum=sum+tint(k)
        continue
    202 END DO
    isgn=1
    IF (tint(ib-1) < tint(ib+1)) THEN
        isgn=-1.0
    ENDIF
    tint(ib)=6*tint(ib-isgn)-5*tint(ib-isgn*2)
    sum=sum+tint(ib)
    temp1=0.0
    temp2=0.0
    do 203 lp=1,smo
        do 204 k=2,nsite-1
            temp1=tint(k)
            tint(k)=(temp2+2*tint(k)+tint(k+1)+1.0e-30)/4
            temp2=temp1
            continue
        204 END DO
        continue
    203 END DO
    pts=5000
    dsum=sum/pts
    ipeak=0
    do 205 i=1,nsite
        wf=fl+float(i-1)
        n=nint(tint(i)/dsum)
        do 206 j=1,n
            ipeak=ipeak+1
            w(ipeak)=wf+((j-1)/n)
            continue
        206 END DO
        continue
    205 END DO
    do 209 k=1,ipeak
        w(k)=w0*w(k)
        continue
    209 END DO
!----------------------------------------------------------------------
!     start lineshape calculation according to Mehring's book, p.61
!----------------------------------------------------------------------
    jfreq=jfreq/(float(ipeak)-1.0)
    ar=float(ipeak)*jfreq+(1.0/t2)
    do 90 j=1,nf
        wf=wfl+dwf*float(j-1)
        l=(0.0,0.0)
        do 100 k=1,ipeak
            l=l+cmplx(1.0,0.0)/cmplx(ar,wf-w(k))
            continue
        100 END DO
        g(j)=real(l/(cmplx(1.0,0.0)-(cmplx(jfreq,0.0)*l)))
        g(j)=g(j)/float(ipeak)
        continue
    90 END DO
!----------------------------------------------------------------------
!     normalize
!----------------------------------------------------------------------
    gmax=0.0
    do 110 i=1,nf
        if(g(i) > gmax) gmax=g(i)
        continue
    110 END DO
!     open(7,file=outfile)
    do 120 i=1,nf
        ppm=fl+df*float(i-1)
        g(i)=g(i)/gmax
        f(i)=ppm
        continue
    120 END DO
    end
    
