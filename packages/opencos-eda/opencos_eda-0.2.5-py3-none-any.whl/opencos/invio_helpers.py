import os

# Given what we'll assume is a CommandDesign (CommandSim?) object, we'll try to
# perform some invio related commands on it.

def write_py_file(command_design_obj:object, py_filename='run_invio.py', v_filename='',
                  blackbox_list=[], **kwargs) -> dict:
    '''Given an eda.CommandDesign object, creates a .py file that can be run

    from invio-py or standalone. Returns a dict with a few details about the generated .py'''


    # Sanity check that command_design_obj has some expected details.
    assert type(getattr(command_design_obj, 'incdirs', None)) is list
    assert type(getattr(command_design_obj, 'files_v', None)) is list
    assert type(getattr(command_design_obj, 'files_sv', None)) is list
    assert type(getattr(command_design_obj, 'files_vhd', None)) is list

    args = getattr(command_design_obj, 'args', dict())
    work_dir = args.get('work-dir', '')

    assert work_dir

    work_dir = os.path.abspath(work_dir)

    lines = [

        'from invio import init, define_macro, add_include_directory, \\',
        '    add_verilog_file, add_sv_file, elaborate, analyze, write_design',
        'import os, shutil',
        '',
        f'for p in ["invio"]:',
        f'    fullp = os.path.join("{work_dir}", p)',
        f'    if not os.path.exists(fullp):',
        f'        os.mkdir(fullp)',
        '',
    ]

    for name,value in command_design_obj.defines.items():
        if name in ['SIMULATION']:
            continue

        if value is None:
            lines.append(f'define_macro("{name}")')
        else:
            value = str(value)
            value = value.replace("'", "\\" + "'")
            value = value.replace('"', "\\" + '"')
            lines.append(f'define_macro("{name}", value="{value}")')

    # We must define SYNTHESIS for oclib_defines.vh to work correctly.
    lines.append(f'define_macro("SYNTHESIS")')

    for path in command_design_obj.incdirs:
        lines.append(f'add_include_directory("{path}")')

    for path in command_design_obj.files_v:
        lines.append(f'add_verilog_file("{path}")')

    for path in command_design_obj.files_sv:
        lines.append(f'add_sv_file("{path}")')

    for path in command_design_obj.files_vhd:
        lines.append(f'add_vhdl_file("{path}")')

    # Note - big assumption here that "module myname" is contained in myname.[v|sv]:
    blackbox_files_list = list()
    for path in command_design_obj.files_v + command_design_obj.files_sv:
        leaf_filename = path.split('/')[-1]
        module_name = ''.join(leaf_filename.split('.')[:-1])
        if module_name in blackbox_list:
            blackbox_files_list.append(path)


    top = args.get('top', None)
    if top is None:
        # Infer the 'top' module as last verilog, SV, or vhdl file.
        tmp_list = command_design_obj.files_v + command_design_obj.files_sv \
            + command_design_obj.files_vhd
        top_fileonly = tmp_list[-1].split('/')[-1]
        top = ''.join(top_fileonly.split('.')[:-1])


    assert top

    if v_filename:
        v_filename = v_filename
    else:
        v_filename = f'{top}.v'


    full_v_filename = os.path.join(work_dir, 'invio', v_filename)
    full_py_filename = os.path.join(work_dir, py_filename)

    ret = {
        'work_dir': work_dir,
        'py_filename': py_filename,
        'v_filename': v_filename,
        'full_v_filename': full_v_filename,
        'full_py_filename': full_py_filename,
        'top': top,
        'blackbox_module_list': blackbox_list,
        'blackbox_files_list': blackbox_files_list,
    }



    lines += [
        'assert analyze()',
        f"assert elaborate('{top}', rtl_elaboration=True, forceBlackbox={blackbox_list})",
        '',
        f"assert write_design('{full_v_filename}')",
        '',
    ]

    # It seems that Invio's write_design(..) will leave a few VERIFIC_MUX and other modules
    # commented out in the .v file. This doesn't work downstream for yosys, so uncomment these
    # with some brute force.

    tmp_v_filename = os.path.join(work_dir, '_tmp.v')

    lines += [
        '',
        '# We also get the joy of uncommenting any VERIFIC_* modules in the generated .v',
        f'with open("{full_v_filename}") as old, open("{tmp_v_filename}", "w") as new:',
        '    in_verific_commented_module = False',
        '    for line in old.readlines():',
        '        # Handle old, modify line:',
        '        if "// module VERIFIC_" in line:',
        '            in_verific_commented_module = True',
        '        if in_verific_commented_module:',
        '            line = line.replace("// ", "")',
        '        if line.startswith("endmodule"):',
        '            in_verific_commented_module = False',
        '        # Write out line to new:',
        '        new.write(line)',
        f'shutil.move("{tmp_v_filename}", ',
        f'            "{full_v_filename}")',
        '',
    ]


    for k,v in ret.items():
        if type(v) is str:
            lines.append(f'## {k} = "{v}"')


    if py_filename:
        outfile = os.path.join(work_dir, py_filename)
        with open(outfile, 'w') as f:
            f.write('\n'.join(lines))


    return ret




def write_verilog(command_design_obj:object, v_filename='', py_filename='run_invio.py',
                  blackbox_list=[], **kwargs) -> dict:
    '''Creates and runs a .py file to run Invio on a CommandDesign oject. Returns a dict with

    information about what was run.'''

    invio_dict = write_py_file( command_design_obj, v_filename=v_filename,
                                py_filename=py_filename, blackbox_list=blackbox_list,
                                **kwargs )

    # exec the python that was created:
    # Do not run this if args['stop-before-compile'] is True:
    if command_design_obj.args.get('stop-before-compile', False):
        pass # skip it.
    else:
        if 'full_py_filename' in invio_dict:
            exec(open(invio_dict['full_py_filename']).read())

    return invio_dict
