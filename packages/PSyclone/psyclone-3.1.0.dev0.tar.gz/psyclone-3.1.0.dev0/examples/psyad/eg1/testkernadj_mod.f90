module adj_testkern_mod
  implicit none
  public

  contains
  subroutine adj_testkern_code(ascalar, field1, field2, field3, npts)
    real, intent(in) :: ascalar
    integer, intent(in) :: npts
    real, dimension(npts), intent(inout) :: field2
    real, dimension(npts), intent(inout) :: field1
    real, dimension(npts), intent(inout) :: field3
    real :: tmp
    real :: tmp2
    real :: tmp3
    integer :: i
    integer :: idx

    tmp = ascalar ** 2
    do idx = UBOUND(field2, dim=1), LBOUND(field2, dim=1), -1
      field3(idx) = field3(idx) + tmp * field2(idx)
      field1(idx) = field1(idx) + field2(idx)
      field2(idx) = 0.0
    enddo
    field1(1) = field1(1) + field2(npts)
    do i = npts, 1, -1
      tmp2 = i * tmp
      tmp3 = 3.0 * tmp2
      field1(i) = field1(i) + field2(i) / tmp2
      field2(i) = field2(i) + field1(i)
      field3(i) = field3(i) + field1(i)
      field1(i) = tmp * field1(i)
    enddo

  end subroutine adj_testkern_code

end module adj_testkern_mod
