program tra_adv
  use extract_psy_data_mod, only : extract_PSyDataType
  use iso_c_binding, only : c_int64_t
  integer, parameter :: wp = 8
  real(kind=wp), allocatable, dimension(:,:,:,:), save :: t3sn
  real(kind=wp), allocatable, dimension(:,:,:,:), save :: t3ns
  real(kind=wp), allocatable, dimension(:,:,:,:), save :: t3ew
  real(kind=wp), allocatable, dimension(:,:,:,:), save :: t3we
  real(kind=wp), allocatable, dimension(:,:,:), save :: tsn
  real(kind=wp), allocatable, dimension(:,:,:), save :: pun
  real(kind=wp), allocatable, dimension(:,:,:), save :: pvn
  real(kind=wp), allocatable, dimension(:,:,:), save :: pwn
  real(kind=wp), allocatable, dimension(:,:,:), save :: mydomain
  real(kind=wp), allocatable, dimension(:,:,:), save :: zslpx
  real(kind=wp), allocatable, dimension(:,:,:), save :: zslpy
  real(kind=wp), allocatable, dimension(:,:,:), save :: zwx
  real(kind=wp), allocatable, dimension(:,:,:), save :: zwy
  real(kind=wp), allocatable, dimension(:,:,:), save :: umask
  real(kind=wp), allocatable, dimension(:,:,:), save :: vmask
  real(kind=wp), allocatable, dimension(:,:,:), save :: tmask
  real(kind=wp), allocatable, dimension(:,:,:), save :: zind
  real(kind=wp), allocatable, dimension(:,:), save :: ztfreez
  real(kind=wp), allocatable, dimension(:,:), save :: rnfmsk
  real(kind=wp), allocatable, dimension(:,:), save :: upsmsk
  real(kind=wp), allocatable, dimension(:), save :: rnfmsk_z
  real(kind=wp) :: zice
  real(kind=wp) :: zu
  real(kind=wp) :: z0u
  real(kind=wp) :: zzwx
  real(kind=wp) :: zv
  real(kind=wp) :: z0v
  real(kind=wp) :: zzwy
  real(kind=wp) :: ztra
  real(kind=wp) :: zbtr
  real(kind=wp) :: zdt
  real(kind=wp) :: zalpha
  real(kind=wp) :: r
  real(kind=wp) :: zw
  real(kind=wp) :: z0w
  integer :: jpi
  integer :: jpj
  integer :: jpk
  integer :: ji
  integer :: jj
  integer :: jk
  integer :: jt
  integer(kind=c_int64_t) :: it
  CHARACTER(LEN = 10) :: env
  type(extract_PSyDataType), save, target :: extract_psy_data
  type(extract_PSyDataType), save, target :: extract_psy_data_1
  type(extract_PSyDataType), save, target :: extract_psy_data_2
  type(extract_PSyDataType), save, target :: extract_psy_data_3

  call get_environment_variable('JPI', env)
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Read_Stmt
  READ(env, '(i10)') jpi
  call get_environment_variable('JPJ', env)
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Read_Stmt
  READ(env, '(i10)') jpj
  call get_environment_variable('JPK', env)
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Read_Stmt
  READ(env, '(i10)') jpk
  call get_environment_variable('IT', env)
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Read_Stmt
  READ(env, '(i10)') it
  ALLOCATE(mydomain(1:jpi,1:jpj,1:jpk))
  ALLOCATE(zwx(1:jpi,1:jpj,1:jpk))
  ALLOCATE(zwy(1:jpi,1:jpj,1:jpk))
  ALLOCATE(zslpx(1:jpi,1:jpj,1:jpk))
  ALLOCATE(zslpy(1:jpi,1:jpj,1:jpk))
  ALLOCATE(pun(1:jpi,1:jpj,1:jpk))
  ALLOCATE(pvn(1:jpi,1:jpj,1:jpk))
  ALLOCATE(pwn(1:jpi,1:jpj,1:jpk))
  ALLOCATE(umask(1:jpi,1:jpj,1:jpk))
  ALLOCATE(vmask(1:jpi,1:jpj,1:jpk))
  ALLOCATE(tmask(1:jpi,1:jpj,1:jpk))
  ALLOCATE(zind(1:jpi,1:jpj,1:jpk))
  ALLOCATE(ztfreez(1:jpi,1:jpj))
  ALLOCATE(rnfmsk(1:jpi,1:jpj))
  ALLOCATE(upsmsk(1:jpi,1:jpj))
  ALLOCATE(rnfmsk_z(1:jpk))
  ALLOCATE(tsn(1:jpi,1:jpj,1:jpk))
  r = jpi * jpj * jpk
  CALL extract_psy_data % PreStart("tra_adv", "r0", 4, 11)
  CALL extract_psy_data % PreDeclareVariable("jpi", jpi)
  CALL extract_psy_data % PreDeclareVariable("jpj", jpj)
  CALL extract_psy_data % PreDeclareVariable("jpk", jpk)
  CALL extract_psy_data % PreDeclareVariable("r", r)
  CALL extract_psy_data % PreDeclareVariable("ji_post", ji)
  CALL extract_psy_data % PreDeclareVariable("jj_post", jj)
  CALL extract_psy_data % PreDeclareVariable("jk_post", jk)
  CALL extract_psy_data % PreDeclareVariable("mydomain_post", mydomain)
  CALL extract_psy_data % PreDeclareVariable("pun_post", pun)
  CALL extract_psy_data % PreDeclareVariable("pvn_post", pvn)
  CALL extract_psy_data % PreDeclareVariable("pwn_post", pwn)
  CALL extract_psy_data % PreDeclareVariable("tmask_post", tmask)
  CALL extract_psy_data % PreDeclareVariable("tsn_post", tsn)
  CALL extract_psy_data % PreDeclareVariable("umask_post", umask)
  CALL extract_psy_data % PreDeclareVariable("vmask_post", vmask)
  CALL extract_psy_data % PreEndDeclaration
  CALL extract_psy_data % ProvideVariable("jpi", jpi)
  CALL extract_psy_data % ProvideVariable("jpj", jpj)
  CALL extract_psy_data % ProvideVariable("jpk", jpk)
  CALL extract_psy_data % ProvideVariable("r", r)
  CALL extract_psy_data % PreEnd
  do jk = 1, jpk, 1
    do jj = 1, jpj, 1
      do ji = 1, jpi, 1
        umask(ji,jj,jk) = ji * jj * jk / r
        mydomain(ji,jj,jk) = ji * jj * jk / r
        pun(ji,jj,jk) = ji * jj * jk / r
        pvn(ji,jj,jk) = ji * jj * jk / r
        pwn(ji,jj,jk) = ji * jj * jk / r
        vmask(ji,jj,jk) = ji * jj * jk / r
        tsn(ji,jj,jk) = ji * jj * jk / r
        tmask(ji,jj,jk) = ji * jj * jk / r
      enddo
    enddo
  enddo
  CALL extract_psy_data % PostStart
  CALL extract_psy_data % ProvideVariable("ji_post", ji)
  CALL extract_psy_data % ProvideVariable("jj_post", jj)
  CALL extract_psy_data % ProvideVariable("jk_post", jk)
  CALL extract_psy_data % ProvideVariable("mydomain_post", mydomain)
  CALL extract_psy_data % ProvideVariable("pun_post", pun)
  CALL extract_psy_data % ProvideVariable("pvn_post", pvn)
  CALL extract_psy_data % ProvideVariable("pwn_post", pwn)
  CALL extract_psy_data % ProvideVariable("tmask_post", tmask)
  CALL extract_psy_data % ProvideVariable("tsn_post", tsn)
  CALL extract_psy_data % ProvideVariable("umask_post", umask)
  CALL extract_psy_data % ProvideVariable("vmask_post", vmask)
  CALL extract_psy_data % PostEnd
  r = jpi * jpj
  CALL extract_psy_data_1 % PreStart("tra_adv", "r1", 3, 5)
  CALL extract_psy_data_1 % PreDeclareVariable("jpi", jpi)
  CALL extract_psy_data_1 % PreDeclareVariable("jpj", jpj)
  CALL extract_psy_data_1 % PreDeclareVariable("r", r)
  CALL extract_psy_data_1 % PreDeclareVariable("ji_post", ji)
  CALL extract_psy_data_1 % PreDeclareVariable("jj_post", jj)
  CALL extract_psy_data_1 % PreDeclareVariable("rnfmsk_post", rnfmsk)
  CALL extract_psy_data_1 % PreDeclareVariable("upsmsk_post", upsmsk)
  CALL extract_psy_data_1 % PreDeclareVariable("ztfreez_post", ztfreez)
  CALL extract_psy_data_1 % PreEndDeclaration
  CALL extract_psy_data_1 % ProvideVariable("jpi", jpi)
  CALL extract_psy_data_1 % ProvideVariable("jpj", jpj)
  CALL extract_psy_data_1 % ProvideVariable("r", r)
  CALL extract_psy_data_1 % PreEnd
  do jj = 1, jpj, 1
    do ji = 1, jpi, 1
      ztfreez(ji,jj) = ji * jj / r
      upsmsk(ji,jj) = ji * jj / r
      rnfmsk(ji,jj) = ji * jj / r
    enddo
  enddo
  CALL extract_psy_data_1 % PostStart
  CALL extract_psy_data_1 % ProvideVariable("ji_post", ji)
  CALL extract_psy_data_1 % ProvideVariable("jj_post", jj)
  CALL extract_psy_data_1 % ProvideVariable("rnfmsk_post", rnfmsk)
  CALL extract_psy_data_1 % ProvideVariable("upsmsk_post", upsmsk)
  CALL extract_psy_data_1 % ProvideVariable("ztfreez_post", ztfreez)
  CALL extract_psy_data_1 % PostEnd
  CALL extract_psy_data_2 % PreStart("tra_adv", "r2", 1, 2)
  CALL extract_psy_data_2 % PreDeclareVariable("jpk", jpk)
  CALL extract_psy_data_2 % PreDeclareVariable("jk_post", jk)
  CALL extract_psy_data_2 % PreDeclareVariable("rnfmsk_z_post", rnfmsk_z)
  CALL extract_psy_data_2 % PreEndDeclaration
  CALL extract_psy_data_2 % ProvideVariable("jpk", jpk)
  CALL extract_psy_data_2 % PreEnd
  do jk = 1, jpk, 1
    rnfmsk_z(jk) = jk / jpk
  enddo
  CALL extract_psy_data_2 % PostStart
  CALL extract_psy_data_2 % ProvideVariable("jk_post", jk)
  CALL extract_psy_data_2 % ProvideVariable("rnfmsk_z_post", rnfmsk_z)
  CALL extract_psy_data_2 % PostEnd
  CALL extract_psy_data_3 % PreStart("tra_adv", "r3", 16, 23)
  CALL extract_psy_data_3 % PreDeclareVariable("it", it)
  CALL extract_psy_data_3 % PreDeclareVariable("jpi", jpi)
  CALL extract_psy_data_3 % PreDeclareVariable("jpj", jpj)
  CALL extract_psy_data_3 % PreDeclareVariable("jpk", jpk)
  CALL extract_psy_data_3 % PreDeclareVariable("mydomain", mydomain)
  CALL extract_psy_data_3 % PreDeclareVariable("pun", pun)
  CALL extract_psy_data_3 % PreDeclareVariable("pvn", pvn)
  CALL extract_psy_data_3 % PreDeclareVariable("pwn", pwn)
  CALL extract_psy_data_3 % PreDeclareVariable("rnfmsk", rnfmsk)
  CALL extract_psy_data_3 % PreDeclareVariable("rnfmsk_z", rnfmsk_z)
  CALL extract_psy_data_3 % PreDeclareVariable("tmask", tmask)
  CALL extract_psy_data_3 % PreDeclareVariable("tsn", tsn)
  CALL extract_psy_data_3 % PreDeclareVariable("umask", umask)
  CALL extract_psy_data_3 % PreDeclareVariable("upsmsk", upsmsk)
  CALL extract_psy_data_3 % PreDeclareVariable("vmask", vmask)
  CALL extract_psy_data_3 % PreDeclareVariable("ztfreez", ztfreez)
  CALL extract_psy_data_3 % PreDeclareVariable("ji_post", ji)
  CALL extract_psy_data_3 % PreDeclareVariable("jj_post", jj)
  CALL extract_psy_data_3 % PreDeclareVariable("jk_post", jk)
  CALL extract_psy_data_3 % PreDeclareVariable("jt_post", jt)
  CALL extract_psy_data_3 % PreDeclareVariable("mydomain_post", mydomain)
  CALL extract_psy_data_3 % PreDeclareVariable("z0u_post", z0u)
  CALL extract_psy_data_3 % PreDeclareVariable("z0v_post", z0v)
  CALL extract_psy_data_3 % PreDeclareVariable("z0w_post", z0w)
  CALL extract_psy_data_3 % PreDeclareVariable("zalpha_post", zalpha)
  CALL extract_psy_data_3 % PreDeclareVariable("zbtr_post", zbtr)
  CALL extract_psy_data_3 % PreDeclareVariable("zdt_post", zdt)
  CALL extract_psy_data_3 % PreDeclareVariable("zice_post", zice)
  CALL extract_psy_data_3 % PreDeclareVariable("zind_post", zind)
  CALL extract_psy_data_3 % PreDeclareVariable("zslpx_post", zslpx)
  CALL extract_psy_data_3 % PreDeclareVariable("zslpy_post", zslpy)
  CALL extract_psy_data_3 % PreDeclareVariable("ztra_post", ztra)
  CALL extract_psy_data_3 % PreDeclareVariable("zu_post", zu)
  CALL extract_psy_data_3 % PreDeclareVariable("zv_post", zv)
  CALL extract_psy_data_3 % PreDeclareVariable("zw_post", zw)
  CALL extract_psy_data_3 % PreDeclareVariable("zwx_post", zwx)
  CALL extract_psy_data_3 % PreDeclareVariable("zwy_post", zwy)
  CALL extract_psy_data_3 % PreDeclareVariable("zzwx_post", zzwx)
  CALL extract_psy_data_3 % PreDeclareVariable("zzwy_post", zzwy)
  CALL extract_psy_data_3 % PreEndDeclaration
  CALL extract_psy_data_3 % ProvideVariable("it", it)
  CALL extract_psy_data_3 % ProvideVariable("jpi", jpi)
  CALL extract_psy_data_3 % ProvideVariable("jpj", jpj)
  CALL extract_psy_data_3 % ProvideVariable("jpk", jpk)
  CALL extract_psy_data_3 % ProvideVariable("mydomain", mydomain)
  CALL extract_psy_data_3 % ProvideVariable("pun", pun)
  CALL extract_psy_data_3 % ProvideVariable("pvn", pvn)
  CALL extract_psy_data_3 % ProvideVariable("pwn", pwn)
  CALL extract_psy_data_3 % ProvideVariable("rnfmsk", rnfmsk)
  CALL extract_psy_data_3 % ProvideVariable("rnfmsk_z", rnfmsk_z)
  CALL extract_psy_data_3 % ProvideVariable("tmask", tmask)
  CALL extract_psy_data_3 % ProvideVariable("tsn", tsn)
  CALL extract_psy_data_3 % ProvideVariable("umask", umask)
  CALL extract_psy_data_3 % ProvideVariable("upsmsk", upsmsk)
  CALL extract_psy_data_3 % ProvideVariable("vmask", vmask)
  CALL extract_psy_data_3 % ProvideVariable("ztfreez", ztfreez)
  CALL extract_psy_data_3 % PreEnd
  do jt = 1, it, 1
    do jk = 1, jpk, 1
      do jj = 1, jpj, 1
        do ji = 1, jpi, 1
          if (tsn(ji,jj,jk) <= ztfreez(ji,jj) + 0.1d0) then
            zice = 1.d0
          else
            zice = 0.d0
          end if
          zind(ji,jj,jk) = MAX(rnfmsk(ji,jj) * rnfmsk_z(jk), upsmsk(ji,jj), zice) * tmask(ji,jj,jk)
          zind(ji,jj,jk) = 1 - zind(ji,jj,jk)
        enddo
      enddo
    enddo
    zwx(:,:,jpk) = 0.e0
    zwy(:,:,jpk) = 0.e0
    do jk = 1, jpk - 1, 1
      do jj = 1, jpj - 1, 1
        do ji = 1, jpi - 1, 1
          zwx(ji,jj,jk) = umask(ji,jj,jk) * (mydomain(ji + 1,jj,jk) - mydomain(ji,jj,jk))
          zwy(ji,jj,jk) = vmask(ji,jj,jk) * (mydomain(ji,jj + 1,jk) - mydomain(ji,jj,jk))
        enddo
      enddo
    enddo
    zslpx(:,:,jpk) = 0.e0
    zslpy(:,:,jpk) = 0.e0
    do jk = 1, jpk - 1, 1
      do jj = 2, jpj, 1
        do ji = 2, jpi, 1
          zslpx(ji,jj,jk) = (zwx(ji,jj,jk) + zwx(ji - 1,jj,jk)) * (0.25d0 + SIGN(0.25d0, zwx(ji,jj,jk) * zwx(ji - 1,jj,jk)))
          zslpy(ji,jj,jk) = (zwy(ji,jj,jk) + zwy(ji,jj - 1,jk)) * (0.25d0 + SIGN(0.25d0, zwy(ji,jj,jk) * zwy(ji,jj - 1,jk)))
        enddo
      enddo
    enddo
    do jk = 1, jpk - 1, 1
      do jj = 2, jpj, 1
        do ji = 2, jpi, 1
          zslpx(ji,jj,jk) = SIGN(1.d0, zslpx(ji,jj,jk)) * MIN(ABS(zslpx(ji,jj,jk)), 2.d0 * ABS(zwx(ji - 1,jj,jk)), 2.d0 * &
&ABS(zwx(ji,jj,jk)))
          zslpy(ji,jj,jk) = SIGN(1.d0, zslpy(ji,jj,jk)) * MIN(ABS(zslpy(ji,jj,jk)), 2.d0 * ABS(zwy(ji,jj - 1,jk)), 2.d0 * &
&ABS(zwy(ji,jj,jk)))
        enddo
      enddo
    enddo
    do jk = 1, jpk - 1, 1
      zdt = 1
      do jj = 2, jpj - 1, 1
        do ji = 2, jpi - 1, 1
          z0u = SIGN(0.5d0, pun(ji,jj,jk))
          zalpha = 0.5d0 - z0u
          zu = z0u - 0.5d0 * pun(ji,jj,jk) * zdt
          zzwx = mydomain(ji + 1,jj,jk) + zind(ji,jj,jk) * (zu * zslpx(ji + 1,jj,jk))
          zzwy = mydomain(ji,jj,jk) + zind(ji,jj,jk) * (zu * zslpx(ji,jj,jk))
          zwx(ji,jj,jk) = pun(ji,jj,jk) * (zalpha * zzwx + (1. - zalpha) * zzwy)
          z0v = SIGN(0.5d0, pvn(ji,jj,jk))
          zalpha = 0.5d0 - z0v
          zv = z0v - 0.5d0 * pvn(ji,jj,jk) * zdt
          zzwx = mydomain(ji,jj + 1,jk) + zind(ji,jj,jk) * (zv * zslpy(ji,jj + 1,jk))
          zzwy = mydomain(ji,jj,jk) + zind(ji,jj,jk) * (zv * zslpy(ji,jj,jk))
          zwy(ji,jj,jk) = pvn(ji,jj,jk) * (zalpha * zzwx + (1.d0 - zalpha) * zzwy)
        enddo
      enddo
    enddo
    do jk = 1, jpk - 1, 1
      do jj = 2, jpj - 1, 1
        do ji = 2, jpi - 1, 1
          zbtr = 1.
          ztra = -zbtr * (zwx(ji,jj,jk) - zwx(ji - 1,jj,jk) + zwy(ji,jj,jk) - zwy(ji,jj - 1,jk))
          mydomain(ji,jj,jk) = mydomain(ji,jj,jk) + ztra
        enddo
      enddo
    enddo
    zwx(:,:,1) = 0.e0
    zwx(:,:,jpk) = 0.e0
    do jk = 2, jpk - 1, 1
      zwx(:,:,jk) = tmask(:,:,jk) * (mydomain(:,:,jk - 1) - mydomain(:,:,jk))
    enddo
    zslpx(:,:,1) = 0.e0
    do jk = 2, jpk - 1, 1
      do jj = 1, jpj, 1
        do ji = 1, jpi, 1
          zslpx(ji,jj,jk) = (zwx(ji,jj,jk) + zwx(ji,jj,jk + 1)) * (0.25d0 + SIGN(0.25d0, zwx(ji,jj,jk) * zwx(ji,jj,jk + 1)))
        enddo
      enddo
    enddo
    do jk = 2, jpk - 1, 1
      do jj = 1, jpj, 1
        do ji = 1, jpi, 1
          zslpx(ji,jj,jk) = SIGN(1.d0, zslpx(ji,jj,jk)) * MIN(ABS(zslpx(ji,jj,jk)), 2.d0 * ABS(zwx(ji,jj,jk + 1)), 2.d0 * &
&ABS(zwx(ji,jj,jk)))
        enddo
      enddo
    enddo
    zwx(:,:,1) = pwn(:,:,1) * mydomain(:,:,1)
    zdt = 1
    zbtr = 1.
    do jk = 1, jpk - 1, 1
      do jj = 2, jpj - 1, 1
        do ji = 2, jpi - 1, 1
          z0w = SIGN(0.5d0, pwn(ji,jj,jk + 1))
          zalpha = 0.5d0 + z0w
          zw = z0w - 0.5d0 * pwn(ji,jj,jk + 1) * zdt * zbtr
          zzwx = mydomain(ji,jj,jk + 1) + zind(ji,jj,jk) * (zw * zslpx(ji,jj,jk + 1))
          zzwy = mydomain(ji,jj,jk) + zind(ji,jj,jk) * (zw * zslpx(ji,jj,jk))
          zwx(ji,jj,jk + 1) = pwn(ji,jj,jk + 1) * (zalpha * zzwx + (1. - zalpha) * zzwy)
        enddo
      enddo
    enddo
    zbtr = 1.
    do jk = 1, jpk - 1, 1
      do jj = 2, jpj - 1, 1
        do ji = 2, jpi - 1, 1
          ztra = -zbtr * (zwx(ji,jj,jk) - zwx(ji,jj,jk + 1))
          mydomain(ji,jj,jk) = ztra
        enddo
      enddo
    enddo
  enddo
  CALL extract_psy_data_3 % PostStart
  CALL extract_psy_data_3 % ProvideVariable("ji_post", ji)
  CALL extract_psy_data_3 % ProvideVariable("jj_post", jj)
  CALL extract_psy_data_3 % ProvideVariable("jk_post", jk)
  CALL extract_psy_data_3 % ProvideVariable("jt_post", jt)
  CALL extract_psy_data_3 % ProvideVariable("mydomain_post", mydomain)
  CALL extract_psy_data_3 % ProvideVariable("z0u_post", z0u)
  CALL extract_psy_data_3 % ProvideVariable("z0v_post", z0v)
  CALL extract_psy_data_3 % ProvideVariable("z0w_post", z0w)
  CALL extract_psy_data_3 % ProvideVariable("zalpha_post", zalpha)
  CALL extract_psy_data_3 % ProvideVariable("zbtr_post", zbtr)
  CALL extract_psy_data_3 % ProvideVariable("zdt_post", zdt)
  CALL extract_psy_data_3 % ProvideVariable("zice_post", zice)
  CALL extract_psy_data_3 % ProvideVariable("zind_post", zind)
  CALL extract_psy_data_3 % ProvideVariable("zslpx_post", zslpx)
  CALL extract_psy_data_3 % ProvideVariable("zslpy_post", zslpy)
  CALL extract_psy_data_3 % ProvideVariable("ztra_post", ztra)
  CALL extract_psy_data_3 % ProvideVariable("zu_post", zu)
  CALL extract_psy_data_3 % ProvideVariable("zv_post", zv)
  CALL extract_psy_data_3 % ProvideVariable("zw_post", zw)
  CALL extract_psy_data_3 % ProvideVariable("zwx_post", zwx)
  CALL extract_psy_data_3 % ProvideVariable("zwy_post", zwy)
  CALL extract_psy_data_3 % ProvideVariable("zzwx_post", zzwx)
  CALL extract_psy_data_3 % ProvideVariable("zzwy_post", zzwy)
  CALL extract_psy_data_3 % PostEnd
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Open_Stmt
  OPEN(UNIT = 4, FILE = 'output.dat', FORM = 'formatted')
  do jk = 1, jpk - 1, 1
    do jj = 2, jpj - 1, 1
      do ji = 2, jpi - 1, 1
        ! PSyclone CodeBlock (unsupported code) reason:
        !  - Unsupported statement: Write_Stmt
        WRITE(4, *) mydomain(ji, jj, jk)
      enddo
    enddo
  enddo
  ! PSyclone CodeBlock (unsupported code) reason:
  !  - Unsupported statement: Close_Stmt
  CLOSE(UNIT = 4)
  DEALLOCATE(mydomain)
  DEALLOCATE(zwx)
  DEALLOCATE(zwy)
  DEALLOCATE(zslpx)
  DEALLOCATE(zslpy)
  DEALLOCATE(pun)
  DEALLOCATE(pvn)
  DEALLOCATE(pwn)
  DEALLOCATE(umask)
  DEALLOCATE(vmask)
  DEALLOCATE(tmask)
  DEALLOCATE(zind)
  DEALLOCATE(ztfreez)
  DEALLOCATE(rnfmsk)
  DEALLOCATE(upsmsk)
  DEALLOCATE(rnfmsk_z)
  DEALLOCATE(tsn)

end program tra_adv
