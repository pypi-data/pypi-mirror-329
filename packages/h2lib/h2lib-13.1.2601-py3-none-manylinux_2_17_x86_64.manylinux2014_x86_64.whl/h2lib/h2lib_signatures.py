# noqa

from h2lib.dll_wrapper import DLLWrapper


class H2LibSignatures():
    def add_sensor(self, sensor_line, index_start, index_stop):
        '''subroutine add_sensor(sensor_line, index_start, index_stop) bind(C, name="add_sensor")
      integer*8 :: index_start, index_stop
      character(kind=c_char, len=1), intent(in)       :: sensor_line(1024)
    end subroutine'''
        return self.get_lib_function('add_sensor')(sensor_line, index_start, index_stop)

    def check_convergence(self, bconv, resq, resg, resd):
        '''subroutine check_convergence(bconv, resq, resg, resd) bind(C, name='check_convergence')
      logical(kind=c_bool), intent(out) :: bconv
      real(c_double), intent(out) :: resq
      real(c_double), intent(out) :: resg
      real(c_double), intent(out) :: resd
    end subroutine'''
        return self.get_lib_function('check_convergence')(bconv, resq, resg, resd)

    def do_system_eigenanalysis(self, include_damping, n_modes, natural_frequencies, damping_ratios, error_code):
        '''subroutine do_system_eigenanalysis(include_damping, n_modes, natural_frequencies, damping_ratios, error_code) &
logical(kind=c_bool), intent(in) :: include_damping
integer(kind=4), intent(in) :: n_modes
real(kind=c_double), dimension(n_modes), intent(out) :: natural_frequencies
real(kind=c_double), dimension(n_modes), intent(out) :: damping_ratios
integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('do_system_eigenanalysis')(include_damping, n_modes, natural_frequencies, damping_ratios, error_code)

    def echo_version(self, ):
        '''subroutine echo_version() BIND(C, NAME='echo_version')
    !DEC$ ATTRIBUTES DLLEXPORT :: echo_version
    !GCC$ ATTRIBUTES DLLEXPORT :: echo_version
    type (tbuildinfo)   :: b
end subroutine'''
        return self.get_lib_function('echo_version')()

    def extern_write_log(self, c_msg, n, dll_name, error, warning):
        '''subroutine extern_write_log(c_msg, n, dll_name, error, warning) bind(C, name="extern_write_log")
            integer, intent(in) :: n
            character(kind=c_char, len=1), intent(in) :: c_msg(n)
            character(kind=c_char), intent(in) :: dll_name(50)
            logical(kind=c_bool), intent(in), optional :: error, warning
    character(kind=c_char, len=1), intent(in) :: c_msg(n_msg)
    integer, intent(in) :: n_msg
    character(kind=c_char), intent(in) :: dll_name(50)
    character(len=50) :: n
    logical(kind=c_bool), intent(in), optional :: error, warning
end subroutine'''
        return self.get_lib_function('extern_write_log')(c_msg, n, dll_name, error, warning)

    def fail(self, str_arr):  # pragma: no cover
        '''subroutine fail(str_arr) bind(C, name='fail')
    character(kind=c_char, len=1), intent(inout)       :: str_arr(255)
  end subroutine'''
        return self.get_lib_function('fail')(str_arr)

    def finalize(self, ):
        '''SUBROUTINE finalize() bind(C, name="finalize")
!DEC$ ATTRIBUTES DLLEXPORT :: finalize
  integer:: i
  real*4:: T2
END SUBROUTINE'''
        return self.get_lib_function('finalize')()

    def getSquare(self, val, restype):
        '''function getSquare(val) result(valSquared) BIND(C, NAME='getSquare')
  !DEC$ ATTRIBUTES DLLEXPORT :: getSquare
        real(RK), intent(in) :: val
        real(RK)             :: valSquared
    end function'''
        return self.get_lib_function('getSquare')(val, restype=restype)

    def getState(self, restype):
        '''function getState() result(val) BIND(C, NAME='getState')
  !DEC$ ATTRIBUTES DLLEXPORT :: getState
        integer             :: val
    end function'''
        return self.get_lib_function('getState')(restype=restype)

    def get_aerosections_forces(self, rotor, Fxyz):
        '''subroutine get_aerosections_forces(rotor, Fxyz) bind(C, name='get_aerosections_forces')
    integer*8, intent(in) :: rotor
    real(c_double),intent(out)::Fxyz(rotors_gl%rotor(rotor)%nbld, rotors_gl%rotor(rotor)%blade(1)%nsec, 3)
  end subroutine'''
        return self.get_lib_function('get_aerosections_forces')(rotor, Fxyz)

    def get_aerosections_moments(self, rotor, Mxyz):
        '''subroutine get_aerosections_moments(rotor, Mxyz) bind(C, name='get_aerosections_moments')
    integer*8, intent(in) :: rotor
    real(c_double),intent(out):: Mxyz(rotors_gl%rotor(rotor)%nbld, rotors_gl%rotor(rotor)%blade(1)%nsec, 3)
  end subroutine'''
        return self.get_lib_function('get_aerosections_moments')(rotor, Mxyz)

    def get_aerosections_position(self, rotor, position):
        '''subroutine get_aerosections_position(rotor, position) bind(C, name="get_aerosections_position")
    integer*8, intent(in) :: rotor
    real(c_double),intent(out)   :: position(rotors_gl%rotor(rotor)%nbld, rotors_gl%rotor(rotor)%blade(1)%nsec, 3)
  end subroutine'''
        return self.get_lib_function('get_aerosections_position')(rotor, position)

    def get_bem_grid(self, rotor, azi, rad):
        '''subroutine get_bem_grid(rotor, azi, rad) bind(C, name="get_bem_grid")
    integer*8, intent(in)               :: rotor
    real(c_double), intent(out)       :: azi(rotors_gl%rotor(rotor)%dyn_induc%bem%nazi)
    real(c_double), intent(out)       :: rad(rotors_gl%rotor(rotor)%dyn_induc%bem%nrad)
  end subroutine'''
        return self.get_lib_function('get_bem_grid')(rotor, azi, rad)

    def get_bem_grid_dim(self, rotor, nazi, nrad):
        '''subroutine get_bem_grid_dim(rotor, nazi, nrad) bind(C, name="get_bem_grid_dim")
    integer*8, intent(in)               :: rotor
    integer*8, intent(out)              :: nazi, nrad
  end subroutine'''
        return self.get_lib_function('get_bem_grid_dim')(rotor, nazi, nrad)

    def get_body_rotation_tensor(self, ibdy, amat, error_code):
        '''subroutine get_body_rotation_tensor(ibdy, amat, error_code) &
    integer(kind=8), intent(in) :: ibdy
    real(kind=c_double), dimension(3, 3), intent(out) :: amat
    integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_body_rotation_tensor')(ibdy, amat, error_code)

    def get_diameter(self, rotor, restype):
        '''function get_diameter(rotor) bind(C, name="get_diameter")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_diameter
    integer*8, intent(in) :: rotor
    Type (Taerorotor),pointer :: rotor_p
    real(c_double)  :: get_diameter
 end function'''
        return self.get_lib_function('get_diameter')(rotor, restype=restype)

    def get_induction_axisymmetric(self, rotor, induction):
        '''subroutine get_induction_axisymmetric(rotor, induction) bind(C, name="get_induction_axisymmetric")
    integer*8, intent(in)        :: rotor
    real(c_double),intent(out)   :: induction(rotors_gl%rotor(rotor)%dyn_induc%bem%nrad)
  end subroutine'''
        return self.get_lib_function('get_induction_axisymmetric')(rotor, induction)

    def get_induction_polargrid(self, rotor, induction):
        '''subroutine get_induction_polargrid(rotor, induction) bind(C, name="get_induction_polargrid")
      integer*8, intent(in)        :: rotor
      real(c_double),intent(out)   :: induction(rotors_gl%rotor(rotor)%dyn_induc%bem%nazi, rotors_gl%rotor(rotor)%dyn_induc%bem%nrad)
  end subroutine'''
        return self.get_lib_function('get_induction_polargrid')(rotor, induction)

    def get_induction_rotoravg(self, rotor, induction):
        '''subroutine get_induction_rotoravg(rotor, induction) bind(C, name="get_induction_rotoravg")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_induction_rotoravg
    integer*8, intent(in)        :: rotor
    real(c_double), intent(out) :: induction
  end subroutine'''
        return self.get_lib_function('get_induction_rotoravg')(rotor, induction)

    def get_nSections(self, rotor, blade, restype):
        '''function get_nSections(rotor, blade) bind(C, name="get_nSections")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_nSections
    integer*8, intent(in) :: rotor, blade
    integer*8             :: get_nSections
  end function'''
        return self.get_lib_function('get_nSections')(rotor, blade, restype=restype)

    def get_nblades(self, rotor, restype):
        '''function get_nblades(rotor) bind(C, name="get_nblades")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_nblades
    integer*8, intent(in) ::  rotor
    integer*8             :: get_nblades
  end function'''
        return self.get_lib_function('get_nblades')(rotor, restype=restype)

    def get_nrotors(self, restype):
        '''function get_nrotors() bind(C, name="get_nrotors")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_nrotors
    integer*8 :: get_nrotors
  end function'''
        return self.get_lib_function('get_nrotors')(restype=restype)

    def get_number_of_bodies_and_constraints(self, nbdy, ncst, error_code):
        '''subroutine get_number_of_bodies_and_constraints(nbdy, ncst, error_code) &
    integer(kind=8), intent(out) :: nbdy
    integer(kind=8), intent(out) :: ncst
    integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_number_of_bodies_and_constraints')(nbdy, ncst, error_code)

    def get_number_of_elements(self, nbdy, nelem, error_code):
        '''subroutine get_number_of_elements(nbdy, nelem, error_code) &
    integer(kind=8), intent(in) :: nbdy
    integer(kind=8), dimension(nbdy), intent(out) :: nelem
    integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_number_of_elements')(nbdy, nelem, error_code)

    def get_rotor_avg_wsp(self, coo, rotor, wsp):
        '''subroutine get_rotor_avg_wsp(coo, rotor, wsp) bind(C, name="get_rotor_avg_wsp")
    integer*8, intent(in) :: rotor
    integer*8, intent(in) :: coo ! 1: global, 2: rotor
    real(c_double), dimension(3):: wsp
  end subroutine'''
        return self.get_lib_function('get_rotor_avg_wsp')(coo, rotor, wsp)

    def get_rotor_orientation(self, rotor, yaw, tilt, azi):
        '''subroutine get_rotor_orientation(rotor, yaw, tilt, azi) bind(C, name="get_rotor_orientation")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_rotor_orientation
    integer*8, intent(in) :: rotor
    real(c_double), intent(out) :: yaw, tilt, azi
  end subroutine'''
        return self.get_lib_function('get_rotor_orientation')(rotor, yaw, tilt, azi)

    def get_rotor_position(self, rotor, position):
        '''subroutine get_rotor_position(rotor, position) bind(C, name="get_rotor_position")
    !DEC$ ATTRIBUTES DLLEXPORT :: get_rotor_position
    integer*8, intent(in) :: rotor
    real(c_double), dimension(3), intent(out) ::  position
  !DEC$ ATTRIBUTES DLLEXPORT :: get_rotor_avg_wsp
    integer*8, intent(in) :: rotor
    integer*8, intent(in) :: coo ! 1: global, 2: rotor
  end subroutine'''
        return self.get_lib_function('get_rotor_position')(rotor, position)

    def get_sensor_info(self, id, name, unit, desc):
        '''subroutine get_sensor_info(id, name, unit, desc) bind(C, name="get_sensor_info")
      integer*8, intent(in) :: id
      character(kind=c_char, len=1), intent(out)       :: name(30), unit(10), desc(512)
    end subroutine'''
        return self.get_lib_function('get_sensor_info')(id, name, unit, desc)

    def get_sensor_values(self, ids, values, n):
        '''subroutine get_sensor_values(ids, values, n) bind(C, name="get_sensor_values")
      integer*8, intent(in) :: n
      integer*8, intent(in) :: ids(n)
      real(c_double), intent(out)        :: values(n)
    end subroutine'''
        return self.get_lib_function('get_sensor_values')(ids, values, n)

    def get_system_eigval_eigvec_with_damping(self, n_modes, ny, eigenvalues, eigenvectors, error_code):
        '''subroutine get_system_eigval_eigvec_with_damping(n_modes, ny, eigenvalues, eigenvectors, error_code) &
integer(kind=4), intent(in) :: n_modes
integer(kind=4), intent(in) :: ny
complex(kind=c_double_complex), dimension(n_modes), intent(out) :: eigenvalues
complex(kind=c_double_complex), dimension(ny, n_modes), intent(out) :: eigenvectors
integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_system_eigval_eigvec_with_damping')(n_modes, ny, eigenvalues, eigenvectors, error_code)

    def get_system_eigval_eigvec_without_damping(self, n_modes, ny, eigenvalues, eigenvectors, error_code):
        '''subroutine get_system_eigval_eigvec_without_damping(n_modes, ny, eigenvalues, eigenvectors, error_code) &
integer(kind=4), intent(in) :: n_modes
integer(kind=4), intent(in) :: ny
real(kind=c_double), dimension(n_modes), intent(out) :: eigenvalues
real(kind=c_double), dimension(ny, n_modes), intent(out) :: eigenvectors
integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_system_eigval_eigvec_without_damping')(n_modes, ny, eigenvalues, eigenvectors, error_code)

    def get_system_matrices(self, n_tdofs, n_rdofs, M, C, K, R, error_code):
        '''subroutine get_system_matrices(n_tdofs, n_rdofs, M, C, K, R, error_code) &
integer(kind=4), intent(in) :: n_tdofs
integer(kind=4), intent(in) :: n_rdofs
real(kind=c_double), dimension(n_rdofs, n_rdofs), intent(out) :: M
real(kind=c_double), dimension(n_rdofs, n_rdofs), intent(out) :: C
real(kind=c_double), dimension(n_rdofs, n_rdofs), intent(out) :: K
real(kind=c_double), dimension(n_tdofs, n_rdofs), intent(out) :: R
integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_system_matrices')(n_tdofs, n_rdofs, M, C, K, R, error_code)

    def get_time(self, time):
        '''subroutine
subroutine'''
        return self.get_lib_function('get_time')(time)

    def get_timoshenko_location(self, ibdy, ielem, l, r1, r12, tes, error_code):
        '''subroutine get_timoshenko_location(ibdy, ielem, l, r1, r12, tes, error_code) &
    integer(kind=8), intent(in) :: ibdy
    integer(kind=8), intent(in) :: ielem
    real(kind=c_double), intent(out) :: l
    real(kind=c_double), dimension(3), intent(out) :: r1
    real(kind=c_double), dimension(3), intent(out) :: r12
    real(kind=c_double), dimension(3,3), intent(out) :: tes
    integer(kind=8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('get_timoshenko_location')(ibdy, ielem, l, r1, r12, tes, error_code)

    def get_version(self, s):
        '''subroutine get_version(s) BIND(C, NAME='get_version')
                character(kind=c_char, len=1), intent(inout)  :: s(255)
            end subroutine'''
        return self.get_lib_function('get_version')(s)

    def init(self, ):
        '''subroutine init() bind(C, name="init")
     !DEC$ ATTRIBUTES DLLEXPORT :: init
    end subroutine'''
        return self.get_lib_function('init')()

    def init_windfield(self, Nxyz, dxyz, box_offset_yz, transport_speed):
        '''subroutine init_windfield(Nxyz, dxyz, box_offset_yz, transport_speed) bind(C, name="init_windfield")
      integer*8, dimension(3), intent(in) :: Nxyz
      real*8              :: transport_speed
    end subroutine'''
        return self.get_lib_function('init_windfield')(Nxyz, dxyz, box_offset_yz, transport_speed)

    def linearize(self, n_tdofs, n_rdofs):
        '''subroutine linearize(n_tdofs, n_rdofs) bind(C, name="linearize")
integer(kind=8), intent(out) :: n_tdofs
integer(kind=8), intent(out) :: n_rdofs
end subroutine'''
        return self.get_lib_function('linearize')(n_tdofs, n_rdofs)

    def loop(self, N, restype):
        '''function loop(N) bind(C, Name='loop')
    !DEC$ ATTRIBUTES DLLEXPORT :: loop
    integer*8, intent(in) :: N
    real(c_double) :: loop,a
    integer*8 :: i, j
  end function'''
        return self.get_lib_function('loop')(N, restype=restype)

    def myfunction(self, int, dbl, restype):
        '''function myfunction(int, dbl) bind(C, name='myfunction')
      !DEC$ ATTRIBUTES DLLEXPORT :: myfunction
      integer*8, intent(in) :: int
      real(c_double), intent(in) :: dbl
      real(c_double) :: myfunction
    end function'''
        return self.get_lib_function('myfunction')(int, dbl, restype=restype)

    def mysubroutine(self, str_arr, dbl_arr):
        '''subroutine mysubroutine(str_arr, dbl_arr) bind(C, name='mysubroutine')
      character(kind=c_char, len=1), intent(inout)       :: str_arr(20)
      real(c_double), intent(inout), dimension(2) :: dbl_arr
    end subroutine'''
        return self.get_lib_function('mysubroutine')(str_arr, dbl_arr)

    def read_input(self, htc_path):
        '''subroutine read_input(htc_path) bind(C, name="read_input")
      character(kind=c_char, len=1), intent(in)       :: htc_path(1024)
    end subroutine'''
        return self.get_lib_function('read_input')(htc_path)

    def run(self, time, restype):
        '''function run(time) bind(C, name='run')
      !DEC$ ATTRIBUTES DLLEXPORT :: run
      real(c_double), intent(in) :: time
      real(c_double) :: run, eps
    end function'''
        return self.get_lib_function('run')(time, restype=restype)

    def setState(self, val):
        '''subroutine setState(val) BIND(C, NAME='setState')
  integer, intent(in) :: val
 end subroutine'''
        return self.get_lib_function('setState')(val)

    def set_aerosections_windspeed(self, rotor, uvw):
        '''subroutine set_aerosections_windspeed(rotor, uvw) bind(C, name="set_aerosections_windspeed")
    integer*8, intent(in) :: rotor
    real(c_double),intent(in)   :: uvw(rotors_gl%rotor(rotor)%nbld, rotors_gl%rotor(rotor)%blade(1)%nsec, 3)
  end subroutine'''
        return self.get_lib_function('set_aerosections_windspeed')(rotor, uvw)

    def set_orientation_base(self, main_body_name,
                             n_rows, mbdy_eulerang_table, angles_in_deg, reset_orientation, mbdy_ini_rotvec_d1,
                             error_code):
        '''subroutine set_orientation_base(main_body_name,  &
character(kind=c_char, len=1), dimension(256), intent(in) :: main_body_name
real(kind=c_double), dimension(n_rows, 3),   intent(in) :: mbdy_eulerang_table
logical(c_bool), intent(in) :: angles_in_deg
logical(c_bool), intent(in) :: reset_orientation
real(kind=c_double), dimension(4),   intent(in) :: mbdy_ini_rotvec_d1
end subroutine'''
        return self.get_lib_function('set_orientation_base')(main_body_name,
                                                             n_rows, mbdy_eulerang_table, angles_in_deg, reset_orientation, mbdy_ini_rotvec_d1,
                                                             error_code)

    def set_orientation_relative(self, main_body_1_name, node_1, main_body_2_name, node_2,
                                 n_rows, mbdy2_eulerang_table, angles_in_deg,
                                 reset_orientation,
                                 mbdy2_ini_rotvec_d1,
                                 error_code):
        '''subroutine set_orientation_relative(main_body_1_name, node_1, main_body_2_name, node_2,  &
character(kind=c_char, len=1),   dimension(256),       intent(in   ) :: main_body_1_name  ! Defined as an array of length 1 characters because of bind.
character(kind=c_char, len=1),   dimension(256),       intent(in   ) :: main_body_2_name  ! Defined as an array of length 1 characters because of bind.
integer(kind=8),                                       intent(in   ) :: node_1
integer(kind=8),                                       intent(in   ) :: node_2
real(kind=c_double),             dimension(n_rows, 3), intent(in   ) :: mbdy2_eulerang_table
logical(c_bool),                                       intent(in   ) :: angles_in_deg
character(kind=c_char, len=256) :: mbdy_1_name  ! Same as main_body_1_name, but as string instead of an array of characters.
character(kind=c_char, len=256) :: mbdy_2_name  ! Same as main_body_2_name, but as string instead of an array of characters.
type(Tmain_body_input), pointer :: main_body_1  ! The main body pointer associated to main_body_1_name.
type(Tmain_body_input), pointer :: main_body_2  ! The main body pointer associated to main_body_1_name.
integer(kind=4) :: node_1_local, node_2_local     ! Internal copy of node_1 and node_2.
real*8, dimension(3) :: eulerang                ! Euler angles associated to 1 row of mbdy2_eulerang_table.
end subroutine'''
        return self.get_lib_function('set_orientation_relative')(main_body_1_name, node_1, main_body_2_name, node_2,
                                                                 n_rows, mbdy2_eulerang_table, angles_in_deg,
                                                                 reset_orientation,
                                                                 mbdy2_ini_rotvec_d1,
                                                                 error_code)

    def set_variable_sensor_value(self, id, value):
        '''subroutine set_variable_sensor_value(id, value) bind(C, name="set_variable_sensor_value")
      integer*8, intent(in) :: id
      real(c_double)        :: value
    end subroutine'''
        return self.get_lib_function('set_variable_sensor_value')(id, value)

    def set_windfield(self, uvw, box_offset_x, time):
        '''subroutine set_windfield(uvw, box_offset_x, time) bind(C, name="set_windfield")
      real*4, intent(in) :: uvw(3, gwsd%TMOD%buffer_points_x,gwsd%TMOD%buffer_points_y,gwsd%TMOD%buffer_points_z)
      real*8, intent(in):: box_offset_x, time
    end subroutine'''
        return self.get_lib_function('set_windfield')(uvw, box_offset_x, time)

    def solver_static_delete(self, ):
        '''subroutine solver_static_delete() &
    !DEC$ ATTRIBUTES DLLEXPORT :: solver_static_delete
end subroutine'''
        return self.get_lib_function('solver_static_delete')()

    def solver_static_init(self, ):
        '''subroutine solver_static_init() &
    !DEC$ ATTRIBUTES DLLEXPORT :: solver_static_init
end subroutine'''
        return self.get_lib_function('solver_static_init')()

    def solver_static_run(self, reset_structure, error_code):
        '''subroutine solver_static_run(reset_structure, error_code) bind(C, name="solver_static_run")
    logical(c_bool), intent(in) :: reset_structure
    integer(8), intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('solver_static_run')(reset_structure, error_code)

    def solver_static_solve(self, error_code):
        '''subroutine solver_static_solve(error_code) &
    integer*8, intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('solver_static_solve')(error_code)

    def solver_static_update(self, error_code):
        '''subroutine solver_static_update(error_code) &
    integer*8, intent(out) :: error_code
end subroutine'''
        return self.get_lib_function('solver_static_update')(error_code)

    def sqr2(self, val):
        '''subroutine sqr2(val) BIND(C, NAME='sqr2')
  integer, intent(inout) :: val
 end subroutine'''
        return self.get_lib_function('sqr2')(val)

    def step(self, restype):
        '''function step() bind(C, name='step')
      !DEC$ ATTRIBUTES DLLEXPORT :: step
      real(c_double) :: step
    end function'''
        return self.get_lib_function('step')(restype=restype)

    def stop_on_error(self, flag):
        '''subroutine stop_on_error(flag) bind(C, name="stop_on_error")
      logical(c_bool), intent(in) :: flag
    end subroutine'''
        return self.get_lib_function('stop_on_error')(flag)

    def structure_reset(self, ):
        '''subroutine structure_reset() bind(C, name="structure_reset")
    !DEC$ ATTRIBUTES DLLEXPORT :: structure_reset
    integer*4 :: i, j
end subroutine'''
        return self.get_lib_function('structure_reset')()

    def test_hdf5(self, ):
        '''subroutine test_hdf5() BIND(C, NAME='test_hdf5')
  !DEC$ ATTRIBUTES DLLEXPORT :: test_hdf5
  INTEGER     ::   hdferr ! Error flag
  CHARACTER(9) :: filename = 'test.hdf5'
  INTEGER(HID_T) :: file_id       ! File identifier
  INTEGER(HID_T) :: H5_Create_file,H5_Open_file      ! File identifier
  type(c_ptr) :: x
 end subroutine'''
        return self.get_lib_function('test_hdf5')()

    def work(self, time, restype):
        '''function work(time) bind(C, Name='work')
    !DEC$ ATTRIBUTES DLLEXPORT :: work
    real(c_double), intent(in) :: time
    real*4 :: start_time, t
    integer*8 :: N, work
  end function'''
        return self.get_lib_function('work')(time, restype=restype)

    def write_output(self, ):
        '''subroutine write_output() bind(C, name="write_output")
      !DEC$ ATTRIBUTES DLLEXPORT :: write_output
      integer        :: nr, dummy=1
      character*10 :: status = 'close'
      Type (Toutvar) :: ov_dummy
    end subroutine'''
        return self.get_lib_function('write_output')()
