  MODULE main_psy
    USE constants_mod, ONLY: r_def, l_def, i_def
    USE field_mod, ONLY: field_type, field_proxy_type
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_initialise_fields(field1, field2, one)
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      REAL(KIND=r_def), intent(in) :: one
      TYPE(field_type), intent(in) :: field1, field2
      INTEGER(KIND=i_def) df
      TYPE(extract_PSyDataType), target, save :: extract_psy_data
      INTEGER(KIND=i_def) loop1_start, loop1_stop
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      REAL(KIND=r_def), pointer, dimension(:) :: field2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field1_data => null()
      TYPE(field_proxy_type) field1_proxy, field2_proxy
      INTEGER(KIND=i_def) undf_aspc1_field1, undf_aspc1_field2
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field1_data => field1_proxy%data
      field2_proxy = field2%get_proxy()
      field2_data => field2_proxy%data
      !
      ! Initialise number of DoFs for aspc1_field1
      !
      undf_aspc1_field1 = field1_proxy%vspace%get_undf()
      !
      ! Initialise number of DoFs for aspc1_field2
      !
      undf_aspc1_field2 = field2_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = undf_aspc1_field1
      loop1_start = 1
      loop1_stop = undf_aspc1_field2
      !
      ! Call our kernels
      !
      !
      ! ExtractStart
      !
      CALL extract_psy_data%PreStart("main", "init", 8, 3)
      CALL extract_psy_data%PreDeclareVariable("loop0_start", loop0_start)
      CALL extract_psy_data%PreDeclareVariable("loop0_stop", loop0_stop)
      CALL extract_psy_data%PreDeclareVariable("loop1_start", loop1_start)
      CALL extract_psy_data%PreDeclareVariable("loop1_stop", loop1_stop)
      CALL extract_psy_data%PreDeclareVariable("one", one)
      CALL extract_psy_data%PreDeclareVariable("df", df)
      CALL extract_psy_data%PreDeclareVariable("field1_data", field1_data)
      CALL extract_psy_data%PreDeclareVariable("field2_data", field2_data)
      CALL extract_psy_data%PreDeclareVariable("df_post", df)
      CALL extract_psy_data%PreDeclareVariable("field1_data_post", field1_data)
      CALL extract_psy_data%PreDeclareVariable("field2_data_post", field2_data)
      CALL extract_psy_data%PreEndDeclaration
      CALL extract_psy_data%ProvideVariable("loop0_start", loop0_start)
      CALL extract_psy_data%ProvideVariable("loop0_stop", loop0_stop)
      CALL extract_psy_data%ProvideVariable("loop1_start", loop1_start)
      CALL extract_psy_data%ProvideVariable("loop1_stop", loop1_stop)
      CALL extract_psy_data%ProvideVariable("one", one)
      CALL extract_psy_data%ProvideVariable("df", df)
      CALL extract_psy_data%ProvideVariable("field1_data", field1_data)
      CALL extract_psy_data%ProvideVariable("field2_data", field2_data)
      CALL extract_psy_data%PreEnd
      DO df = loop0_start, loop0_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field1_data(df) = 0.0_r_def
      END DO
      DO df = loop1_start, loop1_stop, 1
        ! Built-in: setval_c (set a real-valued field to a real scalar value)
        field2_data(df) = one
      END DO
      CALL extract_psy_data%PostStart
      CALL extract_psy_data%ProvideVariable("df_post", df)
      CALL extract_psy_data%ProvideVariable("field1_data_post", field1_data)
      CALL extract_psy_data%ProvideVariable("field2_data_post", field2_data)
      CALL extract_psy_data%PostEnd
      !
      ! ExtractEnd
      !
      !
    END SUBROUTINE invoke_initialise_fields
    SUBROUTINE invoke_testkern_w0(field1, field2, chi, some_logical)
      USE testkern_w0_kernel_mod, ONLY: testkern_w0_code
      USE testkern_w0_kernel_mod, ONLY: some_other_var
      USE dummy_mod, ONLY: dummy_var3
      USE dummy_mod, ONLY: dummy_var2
      USE dummy_mod, ONLY: dummy_var1
      USE extract_psy_data_mod, ONLY: extract_PSyDataType
      LOGICAL(KIND=l_def), intent(in) :: some_logical
      TYPE(field_type), intent(in) :: field1, field2, chi(3)
      INTEGER(KIND=i_def) cell
      TYPE(extract_PSyDataType), target, save :: extract_psy_data
      INTEGER(KIND=i_def) loop0_start, loop0_stop
      INTEGER(KIND=i_def) nlayers_field1
      REAL(KIND=r_def), pointer, dimension(:) :: chi_1_data => null(), chi_2_data => null(), chi_3_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field2_data => null()
      REAL(KIND=r_def), pointer, dimension(:) :: field1_data => null()
      TYPE(field_proxy_type) field1_proxy, field2_proxy, chi_proxy(3)
      INTEGER(KIND=i_def), pointer :: map_w0(:,:) => null()
      INTEGER(KIND=i_def) ndf_w0, undf_w0
      !
      ! Initialise field and/or operator proxies
      !
      field1_proxy = field1%get_proxy()
      field1_data => field1_proxy%data
      field2_proxy = field2%get_proxy()
      field2_data => field2_proxy%data
      chi_proxy(1) = chi(1)%get_proxy()
      chi_1_data => chi_proxy(1)%data
      chi_proxy(2) = chi(2)%get_proxy()
      chi_2_data => chi_proxy(2)%data
      chi_proxy(3) = chi(3)%get_proxy()
      chi_3_data => chi_proxy(3)%data
      !
      ! Initialise number of layers
      !
      nlayers_field1 = field1_proxy%vspace%get_nlayers()
      !
      ! Look-up dofmaps for each function space
      !
      map_w0 => field1_proxy%vspace%get_whole_dofmap()
      !
      ! Initialise number of DoFs for w0
      !
      ndf_w0 = field1_proxy%vspace%get_ndf()
      undf_w0 = field1_proxy%vspace%get_undf()
      !
      ! Set-up all of the loop bounds
      !
      loop0_start = 1
      loop0_stop = field1_proxy%vspace%get_ncell()
      !
      ! Call our kernels
      !
      !
      ! ExtractStart
      !
      CALL extract_psy_data%PreStart("main", "update", 15, 3)
      CALL extract_psy_data%PreDeclareVariable("chi", chi)
      CALL extract_psy_data%PreDeclareVariable("field1_data", field1_data)
      CALL extract_psy_data%PreDeclareVariable("field2_data", field2_data)
      CALL extract_psy_data%PreDeclareVariable("loop0_start", loop0_start)
      CALL extract_psy_data%PreDeclareVariable("loop0_stop", loop0_stop)
      CALL extract_psy_data%PreDeclareVariable("map_w0", map_w0)
      CALL extract_psy_data%PreDeclareVariable("ndf_w0", ndf_w0)
      CALL extract_psy_data%PreDeclareVariable("nlayers_field1", nlayers_field1)
      CALL extract_psy_data%PreDeclareVariable("some_logical", some_logical)
      CALL extract_psy_data%PreDeclareVariable("undf_w0", undf_w0)
      CALL extract_psy_data%PreDeclareVariable("dummy_var1@dummy_mod", dummy_var1)
      CALL extract_psy_data%PreDeclareVariable("dummy_var2@dummy_mod", dummy_var2)
      CALL extract_psy_data%PreDeclareVariable("dummy_var3@dummy_mod", dummy_var3)
      CALL extract_psy_data%PreDeclareVariable("some_other_var@testkern_w0_kernel_mod", some_other_var)
      CALL extract_psy_data%PreDeclareVariable("cell", cell)
      CALL extract_psy_data%PreDeclareVariable("cell_post", cell)
      CALL extract_psy_data%PreDeclareVariable("field1_data_post", field1_data)
      CALL extract_psy_data%PreDeclareVariable("dummy_var1_post@dummy_mod", dummy_var1)
      CALL extract_psy_data%PreEndDeclaration
      CALL extract_psy_data%ProvideVariable("chi", chi)
      CALL extract_psy_data%ProvideVariable("field1_data", field1_data)
      CALL extract_psy_data%ProvideVariable("field2_data", field2_data)
      CALL extract_psy_data%ProvideVariable("loop0_start", loop0_start)
      CALL extract_psy_data%ProvideVariable("loop0_stop", loop0_stop)
      CALL extract_psy_data%ProvideVariable("map_w0", map_w0)
      CALL extract_psy_data%ProvideVariable("ndf_w0", ndf_w0)
      CALL extract_psy_data%ProvideVariable("nlayers_field1", nlayers_field1)
      CALL extract_psy_data%ProvideVariable("some_logical", some_logical)
      CALL extract_psy_data%ProvideVariable("undf_w0", undf_w0)
      CALL extract_psy_data%ProvideVariable("dummy_var1@dummy_mod", dummy_var1)
      CALL extract_psy_data%ProvideVariable("dummy_var2@dummy_mod", dummy_var2)
      CALL extract_psy_data%ProvideVariable("dummy_var3@dummy_mod", dummy_var3)
      CALL extract_psy_data%ProvideVariable("some_other_var@testkern_w0_kernel_mod", some_other_var)
      CALL extract_psy_data%ProvideVariable("cell", cell)
      CALL extract_psy_data%PreEnd
      DO cell = loop0_start, loop0_stop, 1
        CALL testkern_w0_code(nlayers_field1, field1_data, field2_data, chi_1_data, chi_2_data, chi_3_data, some_logical, ndf_w0, &
&undf_w0, map_w0(:,cell))
      END DO
      CALL extract_psy_data%PostStart
      CALL extract_psy_data%ProvideVariable("cell_post", cell)
      CALL extract_psy_data%ProvideVariable("field1_data_post", field1_data)
      CALL extract_psy_data%ProvideVariable("dummy_var1_post@dummy_mod", dummy_var1)
      CALL extract_psy_data%PostEnd
      !
      ! ExtractEnd
      !
      !
    END SUBROUTINE invoke_testkern_w0
  END MODULE main_psy