  MODULE psy_alg
    USE field_mod
    USE kind_params_mod
    IMPLICIT NONE
    CONTAINS
    SUBROUTINE invoke_0_inc_field(fld1, nx, ny, this_step)
      USE profile_psy_data_mod, ONLY: profile_PSyDataType
      TYPE(r2d_field), intent(inout) :: fld1
      INTEGER, intent(inout) :: nx
      INTEGER, intent(inout) :: ny
      INTEGER, intent(inout) :: this_step
      INTEGER j
      INTEGER i
      TYPE(profile_PSyDataType), save, target :: profile_psy_data

      CALL profile_psy_data % PreStart("psy_alg", "invoke_0_inc_field-r0", 0, 0)
      fld1%data_on_device = .true.
      fld1%read_from_device_f => read_from_device
      !$acc enter data copyin(fld1,fld1%data,nx,ny,this_step)
      !$acc parallel default(present)
      !$acc loop independent collapse(2)
      DO j = fld1%internal%ystart, fld1%internal%ystop, 1
        DO i = fld1%internal%xstart, fld1%internal%xstop, 1
          CALL inc_field_code(i, j, fld1%data, nx, ny, this_step)
        END DO
      END DO
      !$acc end parallel
      CALL profile_psy_data % PostEnd

    END SUBROUTINE invoke_0_inc_field
    SUBROUTINE inc_field_code(ji, jj, fld1, nx, ny, istp)
      USE kind_params_mod
      INTEGER, intent(in) :: ji
      INTEGER, intent(in) :: jj
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      REAL(KIND=go_wp), dimension(nx,ny), intent(inout) :: fld1
      INTEGER, intent(in) :: istp

      !$acc routine seq
      fld1(ji,jj) = fld1(ji,jj) + REAL(istp, go_wp)

    END SUBROUTINE inc_field_code
    SUBROUTINE read_from_device(from, to, startx, starty, nx, ny, blocking)
      USE iso_c_binding, ONLY: c_ptr
      USE kind_params_mod, ONLY: go_wp
      TYPE(c_ptr), intent(in) :: from
      REAL(KIND=go_wp), DIMENSION(:, :), INTENT(INOUT), TARGET :: to
      INTEGER, intent(in) :: startx
      INTEGER, intent(in) :: starty
      INTEGER, intent(in) :: nx
      INTEGER, intent(in) :: ny
      LOGICAL, intent(in) :: blocking

      !$acc update host(to)

    END SUBROUTINE read_from_device
  END MODULE psy_alg