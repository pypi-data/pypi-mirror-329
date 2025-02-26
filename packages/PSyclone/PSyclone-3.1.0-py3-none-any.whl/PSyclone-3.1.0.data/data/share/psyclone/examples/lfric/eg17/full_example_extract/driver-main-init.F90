! ================================================== !
! THIS FILE IS CREATED FROM THE JINJA TEMPLATE FILE. !
! DO NOT MODIFY DIRECTLY!                            !
! ================================================== !



! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2023-2025, Science and Technology Facilities Council.
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Author: J. Henrichs, Bureau of Meteorology

module compare_variables_mod

    use, intrinsic :: iso_fortran_env, only : real64, stderr => Error_Unit

    implicit None
    integer, parameter :: MAX_ABS_ERROR  = 1
    integer, parameter :: MAX_REL_ERROR  = 2
    integer, parameter :: L2_DIFF        = 3
    integer, parameter :: L2_COS_SIMILAR = 4
    integer, parameter :: count_0        = 5    ! No error
    integer, parameter :: count_neg_9    = 6    ! 10^-9 > rel error > 0
    integer, parameter :: count_neg_6    = 7    ! 10^-6 > rel error >=10^-9
    integer, parameter :: count_neg_3    = 8    ! 10^-3 > rel error >=10^-6

    integer, parameter :: NUM_RESULTS = 8

    integer, parameter                                        :: MAX_STRING_LENGTH=512
    character(MAX_STRING_LENGTH), dimension(:),   allocatable :: all_names
    real(kind=real64),            dimension(:,:), allocatable :: all_results
    integer                                                   :: current_index = 0

    ! Declare generic interface for Compare:
    interface compare
        module procedure compare_scalar_Char
        module procedure compare_array_1dChar
        module procedure compare_array_2dChar
        module procedure compare_array_3dChar
        module procedure compare_array_4dChar
        module procedure compare_scalar_Int
        module procedure compare_array_1dInt
        module procedure compare_array_2dInt
        module procedure compare_array_3dInt
        module procedure compare_array_4dInt
        module procedure compare_scalar_Logical
        module procedure compare_array_1dLogical
        module procedure compare_array_2dLogical
        module procedure compare_array_3dLogical
        module procedure compare_array_4dLogical
        module procedure compare_scalar_Real
        module procedure compare_array_1dReal
        module procedure compare_array_2dReal
        module procedure compare_array_3dReal
        module procedure compare_array_4dReal
        module procedure compare_scalar_Double
        module procedure compare_array_1dDouble
        module procedure compare_array_2dDouble
        module procedure compare_array_3dDouble
        module procedure compare_array_4dDouble
    end interface

contains

    subroutine compare_init(num_vars)
        implicit none
        integer :: num_vars, error

        allocate(all_names(num_vars), stat=error)
        if (error /= 0) then
            write(stderr,*) "Cannot allocate array for ", num_vars, &
                            " result names."
            stop
        endif
        allocate(all_results(num_vars, NUM_RESULTS), stat=error)
        if (error /= 0) then
            write(stderr,*) "Cannot allocate array for ", num_vars, &
                            " result summaries."
            stop
        endif
        current_index = 0

    end subroutine compare_init

    ! -------------------------------------------------------------------------
    subroutine compare_summary()
        implicit none
        integer :: i, max_name_len
        character(256) :: out_format

        ! First compute the format, based on maximum name length:
        max_name_len = -1

        do i=1, current_index
            if (len(trim(all_names(i))) > max_name_len) then
                max_name_len = len(trim(all_names(i)))
            endif
        enddo

        write(out_format, "('(A',I0)" ) max_name_len
        write(*,out_format//",8A13)") "Variable", "max_abs", "max_rel",&
            "l2_diff", "l2_cos", "identical", "#rel<1E-9", "#rel<1E-6", "#rel<1E-3"

        out_format = trim(out_format)//"' ',8(E12.7,' '))"

        ! Then write out the results for each variable:
        do i=1, current_index
            write(*,out_format) trim(all_names(i)), all_results(i,:)
        enddo

    end subroutine compare_summary

    ! -------------------------------------------------------------------------

    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a scalar character(*)
    !! variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results  will be printed when `compare_summary` is called.

    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    !! @param[in] correct_value The expected value of the variable.
    subroutine compare_scalar_Char(name, value, correct_value)
        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64 
        implicit none
        character(*), intent(in)           :: value, correct_value
        character(*)                   :: name

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (value == correct_value) then
            ! All other values have already been initialised with 0
            all_results(current_Index, L2_COS_SIMILAR) = 1
            all_results(current_Index, COUNT_0       ) = 1
        else   ! Results are different
            ! Set all errors to 1
            all_results(current_index, MAX_ABS_ERROR ) = 1.0
            all_results(current_index, L2_DIFF       ) = 1.0
            all_results(current_index, L2_COS_SIMILAR) = 0.0
            all_results(current_index, MAX_REL_ERROR ) = 1.0
            all_results(current_Index, COUNT_NEG_3   ) = 1
        endif

    end subroutine compare_scalar_Char




    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 1D array of
    !! character(*) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_1dChar(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        character(*), dimension(:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:), allocatable :: double_values
        double precision, dimension(:), allocatable :: double_correct
        double precision, dimension(:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! We convert the correct strings to be a '1', and the computed values to
            ! be either 0 if the strings are different, or 1 otherwise.
            allocate(double_values, source=merge(0.0d0, 1.0d0, values /= correct_values))
            ! We need an array shape of booleans here
            allocate(double_correct, source=merge(1.0d0, 0.0d0, values == values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_1dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 2D array of
    !! character(*) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_2dChar(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        character(*), dimension(:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:), allocatable :: double_values
        double precision, dimension(:,:), allocatable :: double_correct
        double precision, dimension(:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! We convert the correct strings to be a '1', and the computed values to
            ! be either 0 if the strings are different, or 1 otherwise.
            allocate(double_values, source=merge(0.0d0, 1.0d0, values /= correct_values))
            ! We need an array shape of booleans here
            allocate(double_correct, source=merge(1.0d0, 0.0d0, values == values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_2dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 3D array of
    !! character(*) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_3dChar(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        character(*), dimension(:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! We convert the correct strings to be a '1', and the computed values to
            ! be either 0 if the strings are different, or 1 otherwise.
            allocate(double_values, source=merge(0.0d0, 1.0d0, values /= correct_values))
            ! We need an array shape of booleans here
            allocate(double_correct, source=merge(1.0d0, 0.0d0, values == values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_3dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 4D array of
    !! character(*) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_4dChar(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        character(*), dimension(:,:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! We convert the correct strings to be a '1', and the computed values to
            ! be either 0 if the strings are different, or 1 otherwise.
            allocate(double_values, source=merge(0.0d0, 1.0d0, values /= correct_values))
            ! We need an array shape of booleans here
            allocate(double_correct, source=merge(1.0d0, 0.0d0, values == values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_4dChar

    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a scalar integer(kind=int32)
    !! variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results  will be printed when `compare_summary` is called.

    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    !! @param[in] correct_value The expected value of the variable.
    subroutine compare_scalar_Int(name, value, correct_value)
        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64 
        implicit none
        integer(kind=int32), intent(in)           :: value, correct_value
        character(*)                   :: name

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (value == correct_value) then
            ! All other values have already been initialised with 0
            all_results(current_Index, L2_COS_SIMILAR) = 1
            all_results(current_Index, COUNT_0       ) = 1
        else   ! Results are different
            all_results(current_index, MAX_ABS_ERROR ) = correct_value - value
            if (correct_value /= 0) then
                all_results(current_index, MAX_REL_ERROR) = &
                    abs((correct_Value-value)/real(value))
            else
                ! Division by 0
                all_results(current_index, MAX_REL_ERROR) = 1.0
            endif
            if(all_results(current_index, MAX_REL_ERROR) >= 1e-3) then
                all_results(current_Index, COUNT_NEG_3   ) = 1
            else if(all_results(current_index, MAX_REL_ERROR) >= 1e-6) then
                all_results(current_Index, COUNT_NEG_6   ) = 1
            else
                all_results(current_Index, COUNT_NEG_9   ) = 1
            endif
        endif

    end subroutine compare_scalar_Int




    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 1D array of
    !! integer(kind=int32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_1dInt(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        integer(kind=int32), dimension(:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:), allocatable :: double_values
        double precision, dimension(:), allocatable :: double_correct
        double precision, dimension(:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_1dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 2D array of
    !! integer(kind=int32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_2dInt(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        integer(kind=int32), dimension(:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:), allocatable :: double_values
        double precision, dimension(:,:), allocatable :: double_correct
        double precision, dimension(:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_2dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 3D array of
    !! integer(kind=int32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_3dInt(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        integer(kind=int32), dimension(:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_3dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 4D array of
    !! integer(kind=int32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_4dInt(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        integer(kind=int32), dimension(:,:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_4dInt

    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a scalar Logical(kind=4)
    !! variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results  will be printed when `compare_summary` is called.

    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    !! @param[in] correct_value The expected value of the variable.
    subroutine compare_scalar_Logical(name, value, correct_value)
        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64 
        implicit none
        Logical(kind=4), intent(in)           :: value, correct_value
        character(*)                   :: name

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (value .EQV. correct_value) then
            ! All other values have already been initialised with 0
            all_results(current_Index, L2_COS_SIMILAR) = 1
            all_results(current_Index, COUNT_0       ) = 1
        else   ! Results are different
            ! Set all errors to 1
            all_results(current_index, MAX_ABS_ERROR ) = 1.0
            all_results(current_index, L2_DIFF       ) = 1.0
            all_results(current_index, L2_COS_SIMILAR) = 0.0
            all_results(current_index, MAX_REL_ERROR ) = 1.0
            all_results(current_Index, COUNT_NEG_3   ) = 1
        endif

    end subroutine compare_scalar_Logical




    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 1D array of
    !! Logical(kind=4) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_1dLogical(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        Logical(kind=4), dimension(:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:), allocatable :: double_values
        double precision, dimension(:), allocatable :: double_correct
        double precision, dimension(:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values .EQV. correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! Convert the logical values to real to avoid special cases:
            allocate(double_values, source=merge(1.0d0, 0.0d0, values))
            allocate(double_correct, source=merge(1.0d0, 0.0d0, correct_values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_1dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 2D array of
    !! Logical(kind=4) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_2dLogical(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        Logical(kind=4), dimension(:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:), allocatable :: double_values
        double precision, dimension(:,:), allocatable :: double_correct
        double precision, dimension(:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values .EQV. correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! Convert the logical values to real to avoid special cases:
            allocate(double_values, source=merge(1.0d0, 0.0d0, values))
            allocate(double_correct, source=merge(1.0d0, 0.0d0, correct_values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_2dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 3D array of
    !! Logical(kind=4) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_3dLogical(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        Logical(kind=4), dimension(:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values .EQV. correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! Convert the logical values to real to avoid special cases:
            allocate(double_values, source=merge(1.0d0, 0.0d0, values))
            allocate(double_correct, source=merge(1.0d0, 0.0d0, correct_values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_3dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 4D array of
    !! Logical(kind=4) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_4dLogical(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        Logical(kind=4), dimension(:,:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values .EQV. correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
! Convert the logical values to real to avoid special cases:
            allocate(double_values, source=merge(1.0d0, 0.0d0, values))
            allocate(double_correct, source=merge(1.0d0, 0.0d0, correct_values))
            ! Now use the double precision arrays for computing the statistics

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_4dLogical

    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a scalar real(kind=real32)
    !! variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results  will be printed when `compare_summary` is called.

    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    !! @param[in] correct_value The expected value of the variable.
    subroutine compare_scalar_Real(name, value, correct_value)
        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64 
        implicit none
        real(kind=real32), intent(in)           :: value, correct_value
        character(*)                   :: name

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (value == correct_value) then
            ! All other values have already been initialised with 0
            all_results(current_Index, L2_COS_SIMILAR) = 1
            all_results(current_Index, COUNT_0       ) = 1
        else   ! Results are different
            all_results(current_index, MAX_ABS_ERROR ) = correct_value - value
            if (correct_value /= 0) then
                all_results(current_index, MAX_REL_ERROR) = abs((correct_Value-value)/value)
            else
                ! Division by 0
                all_results(current_index, MAX_REL_ERROR) = 1.0
            endif
            if(all_results(current_index, MAX_REL_ERROR) >= 1e-3) then
                all_results(current_Index, COUNT_NEG_3   ) = 1
            else if(all_results(current_index, MAX_REL_ERROR) >= 1e-6) then
                all_results(current_Index, COUNT_NEG_6   ) = 1
            else
                all_results(current_Index, COUNT_NEG_9   ) = 1
            endif
        endif

    end subroutine compare_scalar_Real




    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 1D array of
    !! real(kind=real32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_1dReal(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real32), dimension(:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:), allocatable :: double_values
        double precision, dimension(:), allocatable :: double_correct
        double precision, dimension(:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_1dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 2D array of
    !! real(kind=real32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_2dReal(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real32), dimension(:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:), allocatable :: double_values
        double precision, dimension(:,:), allocatable :: double_correct
        double precision, dimension(:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_2dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 3D array of
    !! real(kind=real32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_3dReal(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real32), dimension(:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_3dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 4D array of
    !! real(kind=real32) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_4dReal(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real32), dimension(:,:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_4dReal

    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a scalar real(kind=real64)
    !! variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results  will be printed when `compare_summary` is called.

    !! @param[in] name The name of the variable (string).
    !! @param[in] value The value of the variable.
    !! @param[in] correct_value The expected value of the variable.
    subroutine compare_scalar_Double(name, value, correct_value)
        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64 
        implicit none
        real(kind=real64), intent(in)           :: value, correct_value
        character(*)                   :: name

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (value == correct_value) then
            ! All other values have already been initialised with 0
            all_results(current_Index, L2_COS_SIMILAR) = 1
            all_results(current_Index, COUNT_0       ) = 1
        else   ! Results are different
            all_results(current_index, MAX_ABS_ERROR ) = correct_value - value
            if (correct_value /= 0) then
                all_results(current_index, MAX_REL_ERROR) = abs((correct_Value-value)/value)
            else
                ! Division by 0
                all_results(current_index, MAX_REL_ERROR) = 1.0
            endif
            if(all_results(current_index, MAX_REL_ERROR) >= 1e-3) then
                all_results(current_Index, COUNT_NEG_3   ) = 1
            else if(all_results(current_index, MAX_REL_ERROR) >= 1e-6) then
                all_results(current_Index, COUNT_NEG_6   ) = 1
            else
                all_results(current_Index, COUNT_NEG_9   ) = 1
            endif
        endif

    end subroutine compare_scalar_Double




    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 1D array of
    !! real(kind=real64) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_1dDouble(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real64), dimension(:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:), allocatable :: double_values
        double precision, dimension(:), allocatable :: double_correct
        double precision, dimension(:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_1dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 2D array of
    !! real(kind=real64) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_2dDouble(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real64), dimension(:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:), allocatable :: double_values
        double precision, dimension(:,:), allocatable :: double_correct
        double precision, dimension(:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_2dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 3D array of
    !! real(kind=real64) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_3dDouble(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real64), dimension(:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_3dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine compares the value of a 4D array of
    !! real(kind=real64) variable with the expected correct value and adds statistics
    !! about this comparison to the global field all_result fields. The
    !! results will be printed when `compare_summary` is called.
    !! @param[in] name The name of the variable (string).
    !! @param[in] values The values of the variable.
    !! @param[in] correct_values The expected value of the variable.
    subroutine compare_array_4dDouble(name, values, correct_values)

        use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                                  real32, real64
        implicit none

        real(kind=real64), dimension(:,:,:,:), intent(in)  :: values, correct_values
        character(*), intent(in)                        :: name

        ! Convert any type to double to be able to use the same maths:
        double precision, dimension(:,:,:,:), allocatable :: double_values
        double precision, dimension(:,:,:,:), allocatable :: double_correct
        double precision, dimension(:,:,:,:), allocatable :: tmp

        current_index = current_index + 1
        all_names(current_index) = name
        all_results(current_index,:) = 0.0
        if (all(values == correct_values)) then
            ! All values correct. Notice that all results are already initialised
            ! to 0, so only set the non-zero values here:
            all_results(current_index, L2_COS_SIMILAR) = 1
            all_results(current_index, COUNT_0       ) = size(correct_values)
        else
            ! There are errors
            allocate(double_values, source=dble(values))
            allocate(double_correct, source=dble(correct_values))

            allocate(tmp, mold=double_values)

            tmp = double_correct - double_values
            all_results(current_index, MAX_ABS_ERROR) = maxval(abs(tmp))
            all_results(current_index, L2_DIFF) = sqrt(real(sum(tmp*tmp)))
            all_results(current_index, L2_COS_SIMILAR) = &
                sum(double_values*double_correct)        &
                / sqrt(real(sum(double_values*double_values)))  &
                / sqrt(real(sum(double_correct*double_correct)))
            all_results(current_index, count_0) = count(tmp == 0.0d0)

            where(double_correct /= 0)
                tmp = abs(tmp/double_correct)
            elsewhere
                tmp = -1
            endwhere
            all_results(current_index, MAX_REL_ERROR) = maxval(tmp)
            all_results(current_index, COUNT_NEG_3) = count(tmp > 1.0d-3)
            ! Count elements >10^-6, and subtract the ones larger than 10^-3
            all_results(current_index, COUNT_NEG_6) = count(tmp > 1.0d-6) &
                - all_results(current_Index, COUNT_NEG_3)
            all_results(current_index, COUNT_NEG_9) = count(tmp > 1.0d-9) &
                - all_results(current_Index, COUNT_NEG_6)

        endif

    end subroutine Compare_array_4dDouble

end module compare_variables_mod



!-----------------------------------------------------------------------------
! Copyright (c) 2017-2025,  Met Office, on behalf of HMSO and Queen's Printer
! For further details please refer to the file LICENCE.original which you
! should have received as part of this distribution.
!-----------------------------------------------------------------------------
! LICENCE.original is available from the Met Office Science Repository Service:
! https://code.metoffice.gov.uk/trac/lfric/browser/LFRic/trunk/LICENCE.original
!-----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Modifications copyright (c) 2017-2025, Science and Technology Facilities
! Council
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
! DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
! FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
! DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
! SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
! OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
! OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
!
!> @brief Define various constants for the application.
!>
!> @details Various computational, physical and geometrical constants are
!>          defined in this module. Their values are also set here.
module constants_mod

  use, intrinsic :: iso_fortran_env, only : int8, int16, int32, int64, &
                                            real32, real64, real128

  implicit none

  private

  public :: c_def, c_native,                                             &
            dp_native, dp_xios,                                          &
            i_byte, i_def, i_halo_index, i_long, i_medium, i_native,     &
            i_timestep, i_um, i_ncdf,                                    &
            l_def, l_native,                                             &
            r_def, r_double, r_ncdf, r_native, r_second, r_single, r_um, &
            r_solver, r_tran, r_bl, r_phys,                              &
            CMDI, UNSET_KEY, EMDI, IMDI, RMDI,                           &
            real_type, r_solver_real_type, r_tran_real_type,             &
            r_bl_real_type, r_phys_real_type,                            &
            integer_type, logical_type,                                  &
            EPS, tiny_eps,                                               &
            str_def, str_long, str_max_filename, str_short,              &
            str_longlong,                                                &
            LARGE_REAL_NEGATIVE, LARGE_REAL_POSITIVE,                    &
            xios_max_int, PI, degrees_to_radians, radians_to_degrees,    &
            cache_block, PRECISION_REAL, PRECISION_R_SOLVER,             &
            PRECISION_R_TRAN, EPS_R_TRAN,                                &
            PRECISION_R_BL, PRECISION_R_PHYS

  ! Define default application-defined kinds for all intrinsic data types

  !> @name Set up default kinds for real and double-precision variables.
  !> @{
  real               :: r_val              !< A native real used to compute kind of native real.
  double precision   :: dp_val             !< A native double-precision used to compute kind of native dp.

  ! Default real kind for application.







  integer,      parameter :: r_def = real64
  character(3), parameter :: PRECISION_REAL = '64'


  ! Default real kind for r_solver.







  integer,      parameter :: r_solver = real64
  character(3), parameter :: PRECISION_R_SOLVER = '64'


  ! Default real kind for r_tran.







  integer,      parameter :: r_tran = real64
  character(3), parameter :: PRECISION_R_TRAN = '64'


  ! Default real kind for r_bl.




  integer,      parameter :: r_bl = real64
  character(3), parameter :: PRECISION_R_BL = '64'


  ! Default real kind for r_phys.




  integer,      parameter :: r_phys = real64
  character(3), parameter :: PRECISION_R_PHYS = '64'


  integer, parameter :: real_type          = 1 !< A parameter used to indicate a real data typa
  integer, parameter :: r_solver_real_type = 1 !< A parameter used to indicate a r_solver data type
  integer, parameter :: r_tran_real_type   = 1 !< A parameter used to indicate a r_tran data type
  integer, parameter :: r_bl_real_type     = 1 !< A parameter used to indicate a r_bl data type
  integer, parameter :: r_phys_real_type   = 1 !< A parameter used to indicate a r_phys data type
  integer, parameter :: integer_type       = 2 !< A parameter used to indicate an integer data type
  integer, parameter :: logical_type       = 3 !< A parameter used to indicate a logical data type

  integer, parameter :: r_double = real64 !< Default double precision real kind for application.
  integer, parameter :: r_native = kind(r_val)  !< Native kind for real.
  integer, parameter :: r_ncdf   = real64 !< Default real kind used in netcdf get and put.
  integer, parameter :: r_quad   = real128 !< Default quad precision real kind for application.
  integer, parameter :: r_second = real64 !< Kind for second counts.
  integer, parameter :: r_single = real32 !< Default single precision real kind for application.
  integer, parameter :: r_um     = real64 !< Default real kind used by the UM.

  integer, parameter :: dp_native = kind(dp_val) !< Native kind for double precision.
  ! Define kinds specifically for IO
  integer, parameter :: dp_xios   = kind(dp_val) !< XIOS kind for double precision fields

  !> @}

  !> @name Complex
  !> @{
  !> @}

  !> @name Set up default kinds for integers.
  !> @{
  integer            :: i_val                      !< A native integer used to compute kind of native integer.

  integer, parameter :: i_byte       = int8        !< Explicit byte integer.
  integer, parameter :: i_def        = int32       !< Default integer kind for application.
  integer, parameter :: i_halo_index = int64       !< Integer kind for the index used in halo swapping
  integer, parameter :: i_long       = int64       !< Explicit long integer.
  integer, parameter :: i_medium     = int32       !< Explicit midsize integer.
  integer, parameter :: i_native     = kind(i_val) !< Native kind for integer.
  integer, parameter :: i_ncdf       = int32       !< Default int kind used in netcdf get and put.
  integer, parameter :: i_short      = int16       !< Explicit short integer.
  integer, parameter :: i_timestep   = int32       !< Kind for timestep counts.
  integer, parameter :: i_um         = int32       !< Default integer kind used by the UM.
  !> @}

  !> @name Set up default kinds for logicals.
  !> @{
  logical            :: l_val                   !< A native logical used to compute kind of native logical.

  integer, parameter :: l_def     = kind(l_val) !< Default logical kind for application.
  integer, parameter :: l_native  = kind(l_val) !< Native kind for logical.
  !> @}

  !> @name Set up default kinds for character variables.
  !> @{
  character          :: c_val                   !< A native character used to compute kind of native character.

  integer, parameter :: c_def     = kind(c_val) !< Default character kind for application.
  integer, parameter :: c_native  = kind(c_val) !< Native kind for character.
  !> @}

  !> @name Set up default lengths for string variables.
  !> @{
  integer, parameter :: str_short        = 16  !< Length of "short" strings.
  integer, parameter :: str_def          = 128 !< Default string length for normal strings.
  integer, parameter :: str_long         = 255 !< Default length of long string.
  integer, parameter :: str_longlong     = 512 !< Default length of longer string.
  integer, parameter :: str_max_filename = 512 !< Default maximum length of a file-name.
  !> @}

  !> @name Platform constants
  !> @{
  real(kind=r_def), parameter    :: LARGE_REAL_POSITIVE = huge(0.0_r_def) !< The largest
  !<                                positive number of kind r_def that is not an infinity.
  real(kind=r_def), parameter    :: LARGE_REAL_NEGATIVE = -LARGE_REAL_POSITIVE !< The largest
  !<                                negative number of kind r_def that is not an infinity.

  integer(kind=i_def), parameter :: xios_max_int = huge(0_i_short) !< The largest
  !<                                integer that can be output by XIOS
  integer, parameter :: cache_block = 256 !< Size of a cache block, for padding
  !<                                arrays to ensure access to different cache lines

  !> @}

  !> @name Numerical constants
  !> @{
  real(kind=r_def), parameter  :: EPS = 3.0e-15_r_def
  !<                              Relative precision: if (abs(x-y) < EPS) then assume x==y.
  real(kind=r_tran), parameter :: EPS_R_TRAN = 3.0e-15_r_def
  !<                              Relative precision: if (abs(x-y) < EPS_R_TRAN) then assume x==y.
  real(kind=r_tran), parameter :: tiny_eps = 1.0e-30_r_tran
  !<                              Similar to EPS but lot smaller, which can be used where
  !<                              x/y < EPS but (x-y) is not considered to be zero like many chemistry tracers.
  !> @}

  !> @name Mathematical constants
  !> @{
  real(kind=r_def), parameter :: PI  = 4.0_r_def*atan(1.0_r_def) !< Value of pi.
  !> @}

  !> @name Conversion factors
  !> @{
  real(r_def), parameter :: degrees_to_radians = PI / 180.0_r_def
  real(r_def), parameter :: radians_to_degrees = 180.0_r_def / PI

  !> @}
  ! Missing data indicators
  real     (r_def),     parameter :: RMDI  = -huge(0.0_r_def) !< Value for real numbers
  integer  (i_def),     parameter :: IMDI  = -huge(0_i_def)   !< Value for integer numbers
  character(str_short), parameter :: CMDI  = 'unset'          !< Value for characters
  character(str_short), parameter :: UNSET_KEY  = CMDI        !< Chararater value for namelist enumerations
  integer  (i_native),  parameter :: EMDI  = -1_i_native      !< Integer value for namelist enumerations

  !> @}

end module constants_mod

! ================================================== !
! THIS FILE IS CREATED FROM THE JINJA TEMPLATE FILE. !
! DO NOT MODIFY DIRECTLY!                            !
! ================================================== !



! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2022-2025, Science and Technology Facilities Council.
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Author: J. Henrichs, Bureau of Meteorology

!> This module implements a simple binary file reader. It provides the
!! functions:
!! OpenRead:      opens a file for reading
!! ReadScalar...:           reads the specified scalar value
!! ReadArray1dDouble, ... : allocates and reads the specified array type.

module read_kernel_data_mod

    use, intrinsic :: iso_fortran_env, only : int64, int32,   &
                                              real32, real64, &
                                              stderr => Error_Unit

    implicit none

    !> This is the data type that manages the information required
    !! to read data from a Fortran binary file created by the
    !! extraction library.

    type, public :: ReadKernelDataType

        !> The unit number to use for output
        integer :: unit_number

    contains

        ! The various procedures used
        procedure :: OpenReadFileName
        procedure :: OpenReadModuleRegion


        procedure :: ReadScalarChar
        procedure :: ReadArray1dChar
        procedure :: ReadArray2dChar
        procedure :: ReadArray3dChar
        procedure :: ReadArray4dChar
        procedure :: ReadScalarInt
        procedure :: ReadArray1dInt
        procedure :: ReadArray2dInt
        procedure :: ReadArray3dInt
        procedure :: ReadArray4dInt
        procedure :: ReadScalarLogical
        procedure :: ReadArray1dLogical
        procedure :: ReadArray2dLogical
        procedure :: ReadArray3dLogical
        procedure :: ReadArray4dLogical
        procedure :: ReadScalarReal
        procedure :: ReadArray1dReal
        procedure :: ReadArray2dReal
        procedure :: ReadArray3dReal
        procedure :: ReadArray4dReal
        procedure :: ReadScalarDouble
        procedure :: ReadArray1dDouble
        procedure :: ReadArray2dDouble
        procedure :: ReadArray3dDouble
        procedure :: ReadArray4dDouble

        !> The generic interface for reading the value of variables.
        !! This is not part of the official PSyData API, but is used in
        !! the drivers created by PSyclone.
        generic, public :: ReadVariable => &
            ReadScalarChar, &
            ReadArray1dChar, &
            ReadArray2dChar, &
            ReadArray3dChar, &
            ReadArray4dChar, &
            ReadScalarInt, &
            ReadArray1dInt, &
            ReadArray2dInt, &
            ReadArray3dInt, &
            ReadArray4dInt, &
            ReadScalarLogical, &
            ReadArray1dLogical, &
            ReadArray2dLogical, &
            ReadArray3dLogical, &
            ReadArray4dLogical, &
            ReadScalarReal, &
            ReadArray1dReal, &
            ReadArray2dReal, &
            ReadArray3dReal, &
            ReadArray4dReal, &
            ReadScalarDouble, &
            ReadArray1dDouble, &
            ReadArray2dDouble, &
            ReadArray3dDouble, &
            ReadArray4dDouble

    end type ReadKernelDataType

contains

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called to open a binary file for reading. The
    !! filename is based on the module and kernel name. This is used by a
    !! driver program that will read a binary file previously created by the
    !! PSyData API.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] module_name The name of the module of the instrumented
    !!            region.
    !! @param[in] region_name The name of the instrumented region.
    subroutine OpenReadModuleRegion(this, module_name, region_name)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: module_name, &
                                                         region_name
        integer :: retval

        open(newunit=this%unit_number, access='sequential',  &
             form="unformatted", status="old",               &
             file=module_name//"-"//region_name//".binary")

    end subroutine OpenReadModuleRegion

    ! -------------------------------------------------------------------------
    !> @brief This subroutine is called to open a binary file for reading. The
    !! filename is specified explicitly (as opposed to be based on module-name
    !! and region name in OpenReadModuleRegion). This is used by a driver
    !! program that will read a binary file previously created by the
    !! PSyData API.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] file_name The name of the binary file to open.
    subroutine OpenReadFileName(this, file_name)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: file_name
        integer :: retval

        open(newunit=this%unit_number, access='sequential',  &
             form="unformatted", status="old",               &
             file=file_name)

    end subroutine OpenReadFileName


    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the value of a scalar character(*)
    !! variable from the binary file and returns it to the user. Note that
    !! this function is not part of the PSyData API, but it is convenient to
    !! have these functions together here. The driver can then be linked with
    !! this PSyData library and will be able to read the files.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value The read value is stored here.
    subroutine ReadScalarChar(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: name
        character(*), intent(out)                            :: value

        integer                                          :: retval, varid

        read(this%unit_number) value

    end subroutine ReadScalarChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 1D array of character(*)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray1dChar(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        character(*), dimension(:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1, &
                            " in ReadArray1dChar."
            stop
        endif

        ! Initialise it with "", so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = ""
        read(this%unit_number) value

    end subroutine ReadArray1dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 2D array of character(*)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray2dChar(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        character(*), dimension(:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2, &
                            " in ReadArray2dChar."
            stop
        endif

        ! Initialise it with "", so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = ""
        read(this%unit_number) value

    end subroutine ReadArray2dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 3D array of character(*)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray3dChar(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        character(*), dimension(:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3, &
                            " in ReadArray3dChar."
            stop
        endif

        ! Initialise it with "", so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = ""
        read(this%unit_number) value

    end subroutine ReadArray3dChar



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 4D array of character(*)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray4dChar(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        character(*), dimension(:,:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3,dim_size4
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3
        read(this%unit_number) dim_size4

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3,dim_size4), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3,dim_size4, &
                            " in ReadArray4dChar."
            stop
        endif

        ! Initialise it with "", so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = ""
        read(this%unit_number) value

    end subroutine ReadArray4dChar


    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the value of a scalar integer(kind=int32)
    !! variable from the binary file and returns it to the user. Note that
    !! this function is not part of the PSyData API, but it is convenient to
    !! have these functions together here. The driver can then be linked with
    !! this PSyData library and will be able to read the files.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value The read value is stored here.
    subroutine ReadScalarInt(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: name
        integer(kind=int32), intent(out)                            :: value

        integer                                          :: retval, varid

        read(this%unit_number) value

    end subroutine ReadScalarInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 1D array of integer(kind=int32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray1dInt(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        integer(kind=int32), dimension(:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1, &
                            " in ReadArray1dInt."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray1dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 2D array of integer(kind=int32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray2dInt(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        integer(kind=int32), dimension(:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2, &
                            " in ReadArray2dInt."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray2dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 3D array of integer(kind=int32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray3dInt(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        integer(kind=int32), dimension(:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3, &
                            " in ReadArray3dInt."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray3dInt



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 4D array of integer(kind=int32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray4dInt(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        integer(kind=int32), dimension(:,:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3,dim_size4
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3
        read(this%unit_number) dim_size4

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3,dim_size4), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3,dim_size4, &
                            " in ReadArray4dInt."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray4dInt


    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the value of a scalar Logical(kind=4)
    !! variable from the binary file and returns it to the user. Note that
    !! this function is not part of the PSyData API, but it is convenient to
    !! have these functions together here. The driver can then be linked with
    !! this PSyData library and will be able to read the files.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value The read value is stored here.
    subroutine ReadScalarLogical(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: name
        Logical(kind=4), intent(out)                            :: value

        integer                                          :: retval, varid

        read(this%unit_number) value

    end subroutine ReadScalarLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 1D array of Logical(kind=4)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray1dLogical(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        Logical(kind=4), dimension(:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1, &
                            " in ReadArray1dLogical."
            stop
        endif

        ! Initialise it with false, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = .false.
        read(this%unit_number) value

    end subroutine ReadArray1dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 2D array of Logical(kind=4)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray2dLogical(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        Logical(kind=4), dimension(:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2, &
                            " in ReadArray2dLogical."
            stop
        endif

        ! Initialise it with false, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = .false.
        read(this%unit_number) value

    end subroutine ReadArray2dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 3D array of Logical(kind=4)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray3dLogical(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        Logical(kind=4), dimension(:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3, &
                            " in ReadArray3dLogical."
            stop
        endif

        ! Initialise it with false, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = .false.
        read(this%unit_number) value

    end subroutine ReadArray3dLogical



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 4D array of Logical(kind=4)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray4dLogical(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        Logical(kind=4), dimension(:,:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3,dim_size4
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3
        read(this%unit_number) dim_size4

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3,dim_size4), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3,dim_size4, &
                            " in ReadArray4dLogical."
            stop
        endif

        ! Initialise it with false, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all.
        value = .false.
        read(this%unit_number) value

    end subroutine ReadArray4dLogical


    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the value of a scalar real(kind=real32)
    !! variable from the binary file and returns it to the user. Note that
    !! this function is not part of the PSyData API, but it is convenient to
    !! have these functions together here. The driver can then be linked with
    !! this PSyData library and will be able to read the files.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value The read value is stored here.
    subroutine ReadScalarReal(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: name
        real(kind=real32), intent(out)                            :: value

        integer                                          :: retval, varid

        read(this%unit_number) value

    end subroutine ReadScalarReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 1D array of real(kind=real32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray1dReal(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real32), dimension(:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1, &
                            " in ReadArray1dReal."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray1dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 2D array of real(kind=real32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray2dReal(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real32), dimension(:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2, &
                            " in ReadArray2dReal."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray2dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 3D array of real(kind=real32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray3dReal(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real32), dimension(:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3, &
                            " in ReadArray3dReal."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray3dReal



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 4D array of real(kind=real32)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray4dReal(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real32), dimension(:,:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3,dim_size4
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3
        read(this%unit_number) dim_size4

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3,dim_size4), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3,dim_size4, &
                            " in ReadArray4dReal."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray4dReal


    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the value of a scalar real(kind=real64)
    !! variable from the binary file and returns it to the user. Note that
    !! this function is not part of the PSyData API, but it is convenient to
    !! have these functions together here. The driver can then be linked with
    !! this PSyData library and will be able to read the files.
    !! @param[in,out] this The instance of the ReadKernelDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value The read value is stored here.
    subroutine ReadScalarDouble(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target :: this
        character(*), intent(in)                         :: name
        real(kind=real64), intent(out)                            :: value

        integer                                          :: retval, varid

        read(this%unit_number) value

    end subroutine ReadScalarDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 1D array of real(kind=real64)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray1dDouble(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real64), dimension(:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1, &
                            " in ReadArray1dDouble."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray1dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 2D array of real(kind=real64)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray2dDouble(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real64), dimension(:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2, &
                            " in ReadArray2dDouble."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray2dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 3D array of real(kind=real64)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray3dDouble(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real64), dimension(:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3, &
                            " in ReadArray3dDouble."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray3dDouble



    ! -------------------------------------------------------------------------
    !> @brief This subroutine reads the values of a 4D array of real(kind=real64)
    !! It allocates memory for the allocatable parameter 'value' to store the
    !! read values which is then returned to the caller. If the memory for the
    !! array cannot be allocated, the application will be stopped.
    !! @param[in,out] this The instance of the extract_PsyDataType.
    !! @param[in] name The name of the variable (string).
    !! @param[out] value An allocatable, unallocated 2d-double precision array
    !!             which is allocated here and stores the values read.
    subroutine ReadArray4dDouble(this, name, value)

        implicit none

        class(ReadKernelDataType), intent(inout), target             :: this
        character(*), intent(in)                                     :: name
        real(kind=real64), dimension(:,:,:,:), allocatable, intent(out) :: value

        integer        :: retval, varid
        integer        :: dim_id
        integer        :: dim_size1,dim_size2,dim_size3,dim_size4
        integer        :: ierr

        ! First read in the sizes:
        read(this%unit_number) dim_size1
        read(this%unit_number) dim_size2
        read(this%unit_number) dim_size3
        read(this%unit_number) dim_size4

        ! Allocate enough space to store the values to be read:
        allocate(value(dim_size1,dim_size2,dim_size3,dim_size4), Stat=ierr)
        if (ierr /= 0) then
            write(stderr,*) "Cannot allocate array for ", name, &
                            " of size ", dim_size1,dim_size2,dim_size3,dim_size4, &
                            " in ReadArray4dDouble."
            stop
        endif

        ! Initialise it with 0.0d0, so that an array comparison will work
        ! even though e.g. boundary areas or so might not be set at all. Note
        ! that the compiler will convert the double precision value to the right
        ! type (e.g. int or single precision).
        value = 0.0d0
        read(this%unit_number) value

    end subroutine ReadArray4dDouble


end module read_kernel_data_mod

program main_init
  use compare_variables_mod, only : compare, compare_init, compare_summary
  use constants_mod, only : i_def, l_def, r_bl, r_def, r_double, r_ncdf, r_second, r_single, r_solver, r_tran, r_um
  use read_kernel_data_mod, only : ReadKernelDataType
  character(:), allocatable :: psydata_filename
  character(:), allocatable :: psydata_arg
  integer(kind=i_def) :: loop0_start
  integer(kind=i_def) :: loop0_stop
  real(kind=r_def), allocatable, dimension(:) :: field1_data
  integer(kind=i_def) :: df
  integer(kind=i_def) :: loop1_start
  integer(kind=i_def) :: loop1_stop
  real(kind=r_def), allocatable, dimension(:) :: field2_data
  real(kind=r_def) :: one
  type(ReadKernelDataType) :: extract_psy_data
  integer :: psydata_len
  integer :: psydata_i
  integer(kind=i_def) :: df_post
  real(kind=r_def), allocatable, dimension(:) :: field1_data_post
  real(kind=r_def), allocatable, dimension(:) :: field2_data_post

  do psydata_i = 1, COMMAND_ARGUMENT_COUNT(), 1
    call get_command_argument(psydata_i, length=psydata_len)
    ! PSyclone CodeBlock (unsupported code) reason:
    !  - Allocate statements with type specifications cannot be handled in the PSyIR
    ALLOCATE(CHARACTER(LEN = psydata_len)::psydata_arg)
    call get_command_argument(psydata_i, psydata_arg, length=psydata_len)
    if (psydata_arg == '--update') then
    else
      ! PSyclone CodeBlock (unsupported code) reason:
      !  - Allocate statements with type specifications cannot be handled in the PSyIR
      ALLOCATE(CHARACTER(LEN = psydata_len)::psydata_filename)
      psydata_filename = psydata_arg
    end if
    DEALLOCATE(psydata_arg)
  enddo
  if (ALLOCATED(psydata_filename)) then
    call extract_psy_data%OpenReadFileName(psydata_filename)
  else
    call extract_psy_data%OpenReadModuleRegion('main', 'init')
  end if
  call extract_psy_data%ReadVariable('loop0_start', loop0_start)
  call extract_psy_data%ReadVariable('loop0_stop', loop0_stop)
  call extract_psy_data%ReadVariable('loop1_start', loop1_start)
  call extract_psy_data%ReadVariable('loop1_stop', loop1_stop)
  call extract_psy_data%ReadVariable('one', one)
  call extract_psy_data%ReadVariable('df', df)
  call extract_psy_data%ReadVariable('field1_data', field1_data)
  call extract_psy_data%ReadVariable('field2_data', field2_data)
  call extract_psy_data%ReadVariable('df_post', df_post)
  call extract_psy_data%ReadVariable('field1_data_post', field1_data_post)
  call extract_psy_data%ReadVariable('field2_data_post', field2_data_post)
  do df = loop0_start, loop0_stop, 1
    ! Built-in: setval_c (set a real-valued field to a real scalar value)
    field1_data(df) = 0.0_r_def
  enddo
  do df = loop1_start, loop1_stop, 1
    ! Built-in: setval_c (set a real-valued field to a real scalar value)
    field2_data(df) = one
  enddo
  call compare_init(3)
  call compare('df', df, df_post)
  call compare('field1_data', field1_data, field1_data_post)
  call compare('field2_data', field2_data, field2_data_post)
  call compare_summary()

end program main_init
