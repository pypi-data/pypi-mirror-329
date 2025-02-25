from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ethernet-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ethernet_interfaces = resolve('ethernet_interfaces')
    l_0_POE_CLASS_MAP = missing
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['arista.avd.range_expand']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.range_expand' found.")
    try:
        t_5 = environment.filters['float']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'float' found.")
    try:
        t_6 = environment.filters['format']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'format' found.")
    try:
        t_7 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_8 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_9 = environment.filters['replace']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No filter named 'replace' found.")
    try:
        t_10 = environment.filters['sort']
    except KeyError:
        @internalcode
        def t_10(*unused):
            raise TemplateRuntimeError("No filter named 'sort' found.")
    try:
        t_11 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_11(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    l_0_POE_CLASS_MAP = {0: '15.40', 1: '4.00', 2: '7.00', 3: '15.40', 4: '30.00', 5: '45.00', 6: '60.00', 7: '75.00', 8: '90.00'}
    context.vars['POE_CLASS_MAP'] = l_0_POE_CLASS_MAP
    context.exported_vars.add('POE_CLASS_MAP')
    for l_1_ethernet_interface in t_3((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
        l_1_encapsulation_cli = resolve('encapsulation_cli')
        l_1_encapsulation_dot1q_cli = resolve('encapsulation_dot1q_cli')
        l_1_client_encapsulation = resolve('client_encapsulation')
        l_1_network_flag = resolve('network_flag')
        l_1_network_encapsulation = resolve('network_encapsulation')
        l_1_dfe_algo_cli = resolve('dfe_algo_cli')
        l_1_dfe_hold_time_cli = resolve('dfe_hold_time_cli')
        l_1_address_locking_cli = resolve('address_locking_cli')
        l_1_host_proxy_cli = resolve('host_proxy_cli')
        l_1_tcp_mss_ceiling_cli = resolve('tcp_mss_ceiling_cli')
        l_1_interface_ip_nat = resolve('interface_ip_nat')
        l_1_hide_passwords = resolve('hide_passwords')
        l_1_poe_link_down_action_cli = resolve('poe_link_down_action_cli')
        l_1_poe_limit_cli = resolve('poe_limit_cli')
        l_1_sorted_vlans_cli = resolve('sorted_vlans_cli')
        l_1_isis_auth_cli = resolve('isis_auth_cli')
        l_1_both_key_ids = resolve('both_key_ids')
        l_1_backup_link_cli = resolve('backup_link_cli')
        l_1_tap_identity_cli = resolve('tap_identity_cli')
        l_1_tap_mac_address_cli = resolve('tap_mac_address_cli')
        l_1_tap_truncation_cli = resolve('tap_truncation_cli')
        l_1_tool_groups = resolve('tool_groups')
        l_1_frequency_cli = resolve('frequency_cli')
        l_1_aaa_config = resolve('aaa_config')
        l_1_actions = resolve('actions')
        l_1_host_mode_cli = resolve('host_mode_cli')
        l_1_auth_cli = resolve('auth_cli')
        l_1_auth_failure_fallback_mba = resolve('auth_failure_fallback_mba')
        _loop_vars = {}
        pass
        yield '!\ninterface '
        yield str(environment.getattr(l_1_ethernet_interface, 'name'))
        yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'comment')):
            pass
            for l_2_comment_line in t_1(context.call(environment.getattr(environment.getattr(l_1_ethernet_interface, 'comment'), 'splitlines'), _loop_vars=_loop_vars), []):
                _loop_vars = {}
                pass
                yield '   !! '
                yield str(l_2_comment_line)
                yield '\n'
            l_2_comment_line = missing
        if t_11(environment.getattr(l_1_ethernet_interface, 'profile')):
            pass
            yield '   profile '
            yield str(environment.getattr(l_1_ethernet_interface, 'profile'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_policy'), 'input')):
            pass
            yield '   traffic-policy input '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_policy'), 'input'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_policy'), 'output')):
            pass
            yield '   traffic-policy output '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_policy'), 'output'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'description')):
            pass
            yield '   description '
            yield str(environment.getattr(l_1_ethernet_interface, 'description'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'shutdown'), True):
            pass
            yield '   shutdown\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'shutdown'), False):
            pass
            yield '   no shutdown\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'load_interval')):
            pass
            yield '   load-interval '
            yield str(environment.getattr(l_1_ethernet_interface, 'load_interval'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'mtu')):
            pass
            yield '   mtu '
            yield str(environment.getattr(l_1_ethernet_interface, 'mtu'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'link_status'), True):
            pass
            yield '   logging event link-status\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'link_status'), False):
            pass
            yield '   no logging event link-status\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bgp'), 'session_tracker')):
            pass
            yield '   bgp session tracker '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bgp'), 'session_tracker'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'l2_protocol'), 'forwarding_profile')):
            pass
            yield '   l2-protocol forwarding profile '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'l2_protocol'), 'forwarding_profile'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'flowcontrol'), 'received')):
            pass
            yield '   flowcontrol receive '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'flowcontrol'), 'received'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'l2_mtu')):
            pass
            yield '   l2 mtu '
            yield str(environment.getattr(l_1_ethernet_interface, 'l2_mtu'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'l2_mru')):
            pass
            yield '   l2 mru '
            yield str(environment.getattr(l_1_ethernet_interface, 'l2_mru'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'congestion_drops'), True):
            pass
            yield '   logging event congestion-drops\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'congestion_drops'), False):
            pass
            yield '   no logging event congestion-drops\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'speed')):
            pass
            yield '   speed '
            yield str(environment.getattr(l_1_ethernet_interface, 'speed'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'enabled'), False):
            pass
            yield '   no error-correction encoding\n'
        else:
            pass
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'fire_code'), True):
                pass
                yield '   error-correction encoding fire-code\n'
            elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'fire_code'), False):
                pass
                yield '   no error-correction encoding fire-code\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'reed_solomon'), True):
                pass
                yield '   error-correction encoding reed-solomon\n'
            elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'error_correction_encoding'), 'reed_solomon'), False):
                pass
                yield '   no error-correction encoding reed-solomon\n'
        if (t_11(environment.getattr(l_1_ethernet_interface, 'mode'), 'access') or t_11(environment.getattr(l_1_ethernet_interface, 'mode'), 'dot1q-tunnel')):
            pass
            if t_11(environment.getattr(l_1_ethernet_interface, 'vlans')):
                pass
                yield '   switchport access vlan '
                yield str(environment.getattr(l_1_ethernet_interface, 'vlans'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'access_vlan')):
            pass
            yield '   switchport access vlan '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'access_vlan'))
            yield '\n'
        if (t_11(environment.getattr(l_1_ethernet_interface, 'mode')) and (environment.getattr(l_1_ethernet_interface, 'mode') in ['trunk', 'trunk phone'])):
            pass
            if t_11(environment.getattr(l_1_ethernet_interface, 'native_vlan_tag'), True):
                pass
                yield '   switchport trunk native vlan tag\n'
            elif t_11(environment.getattr(l_1_ethernet_interface, 'native_vlan')):
                pass
                yield '   switchport trunk native vlan '
                yield str(environment.getattr(l_1_ethernet_interface, 'native_vlan'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'phone'), 'vlan')):
            pass
            yield '   switchport phone vlan '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'phone'), 'vlan'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'phone'), 'trunk')):
            pass
            yield '   switchport phone trunk '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'phone'), 'trunk'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan_tag'), True):
            pass
            yield '   switchport trunk native vlan tag\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan')):
            pass
            yield '   switchport trunk native vlan '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'native_vlan'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'phone'), 'vlan')):
            pass
            yield '   switchport phone vlan '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'phone'), 'vlan'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'phone'), 'trunk')):
            pass
            yield '   switchport phone trunk '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'phone'), 'trunk'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'in_required'), True):
            pass
            yield '   switchport vlan translation in required\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'out_required'), True):
            pass
            yield '   switchport vlan translation out required\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'dot1q'), 'vlan_tag')):
            pass
            yield '   switchport dot1q vlan tag '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'dot1q'), 'vlan_tag'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'mode'), 'trunk'):
            pass
            if t_11(environment.getattr(l_1_ethernet_interface, 'vlans')):
                pass
                yield '   switchport trunk allowed vlan '
                yield str(environment.getattr(l_1_ethernet_interface, 'vlans'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan')):
            pass
            yield '   switchport trunk allowed vlan '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'allowed_vlan'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'mode')):
            pass
            yield '   switchport mode '
            yield str(environment.getattr(l_1_ethernet_interface, 'mode'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'mode')):
            pass
            yield '   switchport mode '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'mode'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'dot1q'), 'ethertype')):
            pass
            yield '   switchport dot1q ethertype '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'dot1q'), 'ethertype'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_forwarding_accept_all'), True):
            pass
            yield '   switchport vlan forwarding accept all\n'
        for l_2_trunk_group in t_3(environment.getattr(l_1_ethernet_interface, 'trunk_groups')):
            _loop_vars = {}
            pass
            yield '   switchport trunk group '
            yield str(l_2_trunk_group)
            yield '\n'
        l_2_trunk_group = missing
        for l_2_trunk_group in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'groups')):
            _loop_vars = {}
            pass
            yield '   switchport trunk group '
            yield str(l_2_trunk_group)
            yield '\n'
        l_2_trunk_group = missing
        if t_11(environment.getattr(l_1_ethernet_interface, 'type'), 'routed'):
            pass
            yield '   no switchport\n'
        elif (t_1(environment.getattr(l_1_ethernet_interface, 'type')) in ['l3dot1q', 'l2dot1q']):
            pass
            if (t_11(environment.getattr(l_1_ethernet_interface, 'vlan_id')) and (environment.getattr(l_1_ethernet_interface, 'type') == 'l2dot1q')):
                pass
                yield '   vlan id '
                yield str(environment.getattr(l_1_ethernet_interface, 'vlan_id'))
                yield '\n'
            if t_11(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q_vlan')):
                pass
                yield '   encapsulation dot1q vlan '
                yield str(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q_vlan'))
                yield '\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan')):
                pass
                l_1_encapsulation_cli = str_join(('client dot1q ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'vlan'), ))
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan')):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network dot1q ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'vlan'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'client'), True):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network client', ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            elif (t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner')) and t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'))):
                pass
                l_1_encapsulation_cli = str_join(('client dot1q outer ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'outer'), ' inner ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'dot1q'), 'inner'), ))
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                if (t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner')) and t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'))):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network dot1q outer ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'outer'), ' inner ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'inner'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                elif t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'dot1q'), 'client'), True):
                    pass
                    l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network client', ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'unmatched'), True):
                pass
                l_1_encapsulation_cli = 'client unmatched'
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            if t_11((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli)):
                pass
                yield '   encapsulation vlan\n      '
                yield str((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli))
                yield '\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'type'), 'switched'):
            pass
            yield '   switchport\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'enabled'), True):
            pass
            yield '   switchport\n'
        elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'enabled'), False):
            pass
            yield '   no switchport\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'vlan')):
            pass
            l_1_encapsulation_dot1q_cli = str_join(('encapsulation dot1q vlan ', environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'vlan'), ))
            _loop_vars['encapsulation_dot1q_cli'] = l_1_encapsulation_dot1q_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'inner_vlan')):
                pass
                l_1_encapsulation_dot1q_cli = str_join(((undefined(name='encapsulation_dot1q_cli') if l_1_encapsulation_dot1q_cli is missing else l_1_encapsulation_dot1q_cli), ' inner ', environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'inner_vlan'), ))
                _loop_vars['encapsulation_dot1q_cli'] = l_1_encapsulation_dot1q_cli
            yield '   '
            yield str((undefined(name='encapsulation_dot1q_cli') if l_1_encapsulation_dot1q_cli is missing else l_1_encapsulation_dot1q_cli))
            yield '\n'
        if (t_11(environment.getattr(l_1_ethernet_interface, 'vlan_id')) and (t_1(environment.getattr(l_1_ethernet_interface, 'type')) != 'l2dot1q')):
            pass
            yield '   vlan id '
            yield str(environment.getattr(l_1_ethernet_interface, 'vlan_id'))
            yield '\n'
        if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'encapsulation')) and (not t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_dot1q'), 'vlan')))):
            pass
            l_1_client_encapsulation = environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'encapsulation')
            _loop_vars['client_encapsulation'] = l_1_client_encapsulation
            l_1_network_flag = False
            _loop_vars['network_flag'] = l_1_network_flag
            if ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['dot1q', 'dot1ad']):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'vlan')):
                    pass
                    l_1_encapsulation_cli = str_join(('client ', (undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'vlan'), ))
                    _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                elif (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan')) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'))):
                    pass
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_encapsulation')):
                        pass
                        l_1_encapsulation_cli = str_join(('client ', (undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_encapsulation'), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    else:
                        pass
                        l_1_encapsulation_cli = str_join(('client ', (undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'inner_vlan'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    if (t_1(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'encapsulation')) == 'client inner'):
                        pass
                        l_1_network_flag = True
                        _loop_vars['network_flag'] = l_1_network_flag
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'encapsulation'), ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            elif ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['untagged', 'unmatched']):
                pass
                l_1_encapsulation_cli = str_join(('client ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'client'), 'encapsulation'), ))
                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
            if t_11((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli)):
                pass
                if ((((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) in ['dot1q', 'dot1ad', 'untagged']) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'encapsulation'))) and (not (undefined(name='network_flag') if l_1_network_flag is missing else l_1_network_flag))):
                    pass
                    l_1_network_encapsulation = environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'encapsulation')
                    _loop_vars['network_encapsulation'] = l_1_network_encapsulation
                    if ((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) in ['dot1q', 'dot1ad']):
                        pass
                        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'vlan')):
                            pass
                            l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', (undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'vlan'), ))
                            _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                        elif (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan')) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'))):
                            pass
                            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_encapsulation')):
                                pass
                                l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', (undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_encapsulation'), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'), ))
                                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                            else:
                                pass
                                l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network ', (undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation), ' outer ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'outer_vlan'), ' inner ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'encapsulation_vlan'), 'network'), 'inner_vlan'), ))
                                _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    elif (((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) == 'untagged') and ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) == 'untagged')):
                        pass
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network untagged', ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                    elif (((undefined(name='network_encapsulation') if l_1_network_encapsulation is missing else l_1_network_encapsulation) == 'client') and ((undefined(name='client_encapsulation') if l_1_client_encapsulation is missing else l_1_client_encapsulation) != 'untagged')):
                        pass
                        l_1_encapsulation_cli = str_join(((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli), ' network client', ))
                        _loop_vars['encapsulation_cli'] = l_1_encapsulation_cli
                yield '   encapsulation vlan\n      '
                yield str((undefined(name='encapsulation_cli') if l_1_encapsulation_cli is missing else l_1_encapsulation_cli))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'source_interface')):
            pass
            yield '   switchport source-interface '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'source_interface'))
            yield '\n'
        for l_2_vlan_translation in t_3(environment.getattr(l_1_ethernet_interface, 'vlan_translations')):
            l_2_vlan_translation_cli = resolve('vlan_translation_cli')
            _loop_vars = {}
            pass
            if (t_11(environment.getattr(l_2_vlan_translation, 'from')) and t_11(environment.getattr(l_2_vlan_translation, 'to'))):
                pass
                l_2_vlan_translation_cli = 'switchport vlan translation'
                _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                if (t_1(environment.getattr(l_2_vlan_translation, 'direction')) in ['in', 'out']):
                    pass
                    l_2_vlan_translation_cli = str_join(((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli), ' ', environment.getattr(l_2_vlan_translation, 'direction'), ))
                    _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                l_2_vlan_translation_cli = str_join(((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli), ' ', environment.getattr(l_2_vlan_translation, 'from'), ))
                _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                l_2_vlan_translation_cli = str_join(((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
                _loop_vars['vlan_translation_cli'] = l_2_vlan_translation_cli
                yield '   '
                yield str((undefined(name='vlan_translation_cli') if l_2_vlan_translation_cli is missing else l_2_vlan_translation_cli))
                yield '\n'
        l_2_vlan_translation = l_2_vlan_translation_cli = missing
        for l_2_vlan_translation in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_both'), 'from'):
            l_2_vlan_translation_both_cli = missing
            _loop_vars = {}
            pass
            l_2_vlan_translation_both_cli = str_join(('switchport vlan translation ', environment.getattr(l_2_vlan_translation, 'from'), ))
            _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            if t_11(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), True):
                pass
                l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' dot1q-tunnel', ))
                _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            elif t_11(environment.getattr(l_2_vlan_translation, 'inner_vlan_from')):
                pass
                l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' inner ', environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), ))
                _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
                if t_11(environment.getattr(l_2_vlan_translation, 'network'), True):
                    pass
                    l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' network', ))
                    _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            l_2_vlan_translation_both_cli = str_join(((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
            _loop_vars['vlan_translation_both_cli'] = l_2_vlan_translation_both_cli
            yield '   '
            yield str((undefined(name='vlan_translation_both_cli') if l_2_vlan_translation_both_cli is missing else l_2_vlan_translation_both_cli))
            yield '\n'
        l_2_vlan_translation = l_2_vlan_translation_both_cli = missing
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_in')):
            pass
            for l_2_vlan_translation in environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_in'):
                l_2_vlan_translation_in_cli = missing
                _loop_vars = {}
                pass
                l_2_vlan_translation_in_cli = str_join(('switchport vlan translation in ', environment.getattr(l_2_vlan_translation, 'from'), ))
                _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                if t_11(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel'), True):
                    pass
                    l_2_vlan_translation_in_cli = str_join(((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli), ' dot1q-tunnel', ))
                    _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                elif t_11(environment.getattr(l_2_vlan_translation, 'inner_vlan_from')):
                    pass
                    l_2_vlan_translation_in_cli = str_join(((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli), ' inner ', environment.getattr(l_2_vlan_translation, 'inner_vlan_from'), ))
                    _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                l_2_vlan_translation_in_cli = str_join(((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
                _loop_vars['vlan_translation_in_cli'] = l_2_vlan_translation_in_cli
                yield '   '
                yield str((undefined(name='vlan_translation_in_cli') if l_2_vlan_translation_in_cli is missing else l_2_vlan_translation_in_cli))
                yield '\n'
            l_2_vlan_translation = l_2_vlan_translation_in_cli = missing
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_out')):
            pass
            for l_2_vlan_translation in environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'vlan_translations'), 'direction_out'):
                l_2_vlan_translation_out_cli = resolve('vlan_translation_out_cli')
                _loop_vars = {}
                pass
                if t_11(environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to')):
                    pass
                    l_2_vlan_translation_out_cli = str_join(('switchport vlan translation out ', environment.getattr(l_2_vlan_translation, 'from'), ' dot1q-tunnel ', environment.getattr(l_2_vlan_translation, 'dot1q_tunnel_to'), ))
                    _loop_vars['vlan_translation_out_cli'] = l_2_vlan_translation_out_cli
                elif t_11(environment.getattr(l_2_vlan_translation, 'to')):
                    pass
                    l_2_vlan_translation_out_cli = str_join(('switchport vlan translation out ', environment.getattr(l_2_vlan_translation, 'from'), ' ', environment.getattr(l_2_vlan_translation, 'to'), ))
                    _loop_vars['vlan_translation_out_cli'] = l_2_vlan_translation_out_cli
                    if t_11(environment.getattr(l_2_vlan_translation, 'inner_vlan_to')):
                        pass
                        l_2_vlan_translation_out_cli = str_join(((undefined(name='vlan_translation_out_cli') if l_2_vlan_translation_out_cli is missing else l_2_vlan_translation_out_cli), ' inner ', environment.getattr(l_2_vlan_translation, 'inner_vlan_to'), ))
                        _loop_vars['vlan_translation_out_cli'] = l_2_vlan_translation_out_cli
                if t_11((undefined(name='vlan_translation_out_cli') if l_2_vlan_translation_out_cli is missing else l_2_vlan_translation_out_cli)):
                    pass
                    yield '   '
                    yield str((undefined(name='vlan_translation_out_cli') if l_2_vlan_translation_out_cli is missing else l_2_vlan_translation_out_cli))
                    yield '\n'
            l_2_vlan_translation = l_2_vlan_translation_out_cli = missing
        if t_11(environment.getattr(l_1_ethernet_interface, 'trunk_private_vlan_secondary'), True):
            pass
            yield '   switchport trunk private-vlan secondary\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'trunk_private_vlan_secondary'), False):
            pass
            yield '   no switchport trunk private-vlan secondary\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'trunk'), 'private_vlan_secondary'), True):
            pass
            yield '   switchport trunk private-vlan secondary\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'pvlan_mapping')):
            pass
            yield '   switchport pvlan mapping '
            yield str(environment.getattr(l_1_ethernet_interface, 'pvlan_mapping'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'pvlan_mapping')):
            pass
            yield '   switchport pvlan mapping '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'pvlan_mapping'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'l2_protocol'), 'encapsulation_dot1q_vlan')):
            pass
            yield '   l2-protocol encapsulation dot1q vlan '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'l2_protocol'), 'encapsulation_dot1q_vlan'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'mac_timestamp')):
            pass
            yield '   mac timestamp '
            yield str(environment.getattr(l_1_ethernet_interface, 'mac_timestamp'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment')):
            pass
            yield '   !\n   evpn ethernet-segment\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'identifier')):
                pass
                yield '      identifier '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'identifier'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'redundancy')):
                pass
                yield '      redundancy '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'redundancy'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election')):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'algorithm'), 'modulus'):
                    pass
                    yield '      designated-forwarder election algorithm modulus\n'
                elif (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'algorithm'), 'preference') and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'preference_value'))):
                    pass
                    l_1_dfe_algo_cli = str_join(('designated-forwarder election algorithm preference ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'preference_value'), ))
                    _loop_vars['dfe_algo_cli'] = l_1_dfe_algo_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'dont_preempt'), True):
                        pass
                        l_1_dfe_algo_cli = str_join(((undefined(name='dfe_algo_cli') if l_1_dfe_algo_cli is missing else l_1_dfe_algo_cli), ' dont-preempt', ))
                        _loop_vars['dfe_algo_cli'] = l_1_dfe_algo_cli
                    yield '      '
                    yield str((undefined(name='dfe_algo_cli') if l_1_dfe_algo_cli is missing else l_1_dfe_algo_cli))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'hold_time')):
                    pass
                    l_1_dfe_hold_time_cli = str_join(('designated-forwarder election hold-time ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'hold_time'), ))
                    _loop_vars['dfe_hold_time_cli'] = l_1_dfe_hold_time_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'subsequent_hold_time')):
                        pass
                        l_1_dfe_hold_time_cli = str_join(((undefined(name='dfe_hold_time_cli') if l_1_dfe_hold_time_cli is missing else l_1_dfe_hold_time_cli), ' subsequent-hold-time ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'subsequent_hold_time'), ))
                        _loop_vars['dfe_hold_time_cli'] = l_1_dfe_hold_time_cli
                    yield '      '
                    yield str((undefined(name='dfe_hold_time_cli') if l_1_dfe_hold_time_cli is missing else l_1_dfe_hold_time_cli))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'candidate_reachability_required'), True):
                    pass
                    yield '      designated-forwarder election candidate reachability required\n'
                elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'designated_forwarder_election'), 'candidate_reachability_required'), False):
                    pass
                    yield '      no designated-forwarder election candidate reachability required\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time')):
                pass
                yield '      mpls tunnel flood filter time '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'mpls'), 'tunnel_flood_filter_time'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index')):
                pass
                yield '      mpls shared index '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'mpls'), 'shared_index'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'route_target')):
                pass
                yield '      route-target import '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'evpn_ethernet_segment'), 'route_target'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'flow_tracker'), 'hardware')):
            pass
            yield '   flow tracker hardware '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'flow_tracker'), 'hardware'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'flow_tracker'), 'sampled')):
            pass
            yield '   flow tracker sampled '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'flow_tracker'), 'sampled'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'snmp_trap_link_change'), False):
            pass
            yield '   no snmp trap link-change\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'snmp_trap_link_change'), True):
            pass
            yield '   snmp trap link-change\n'
        if ((t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'address_family'), 'ipv4')) or t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'address_family'), 'ipv6'))) or t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'ipv4_enforcement_disabled'), True)):
            pass
            yield '   !\n   address locking\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'address_family'), 'ipv4'), True):
                pass
                yield '      address-family ipv4\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'address_family'), 'ipv6'), True):
                pass
                yield '      address-family ipv6\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'address_family'), 'ipv4'), False):
                pass
                yield '      address-family ipv4 disabled\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'address_family'), 'ipv6'), False):
                pass
                yield '      address-family ipv6 disabled\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'ipv4_enforcement_disabled'), True):
                pass
                yield '      locked-address ipv4 enforcement disabled\n'
        elif (t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'ipv4'), True) or t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'ipv6'), True)):
            pass
            l_1_address_locking_cli = 'address locking'
            _loop_vars['address_locking_cli'] = l_1_address_locking_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'ipv4'), True):
                pass
                l_1_address_locking_cli = ((undefined(name='address_locking_cli') if l_1_address_locking_cli is missing else l_1_address_locking_cli) + ' ipv4')
                _loop_vars['address_locking_cli'] = l_1_address_locking_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'address_locking'), 'ipv6'), True):
                pass
                l_1_address_locking_cli = ((undefined(name='address_locking_cli') if l_1_address_locking_cli is missing else l_1_address_locking_cli) + ' ipv6')
                _loop_vars['address_locking_cli'] = l_1_address_locking_cli
            yield '   '
            yield str((undefined(name='address_locking_cli') if l_1_address_locking_cli is missing else l_1_address_locking_cli))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'vrf')):
            pass
            yield '   vrf '
            yield str(environment.getattr(l_1_ethernet_interface, 'vrf'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ip_proxy_arp'), True):
            pass
            yield '   ip proxy-arp\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ip_address')):
            pass
            yield '   ip address '
            yield str(environment.getattr(l_1_ethernet_interface, 'ip_address'))
            yield '\n'
            for l_2_ip_address_secondary in t_3(environment.getattr(l_1_ethernet_interface, 'ip_address_secondaries')):
                _loop_vars = {}
                pass
                yield '   ip address '
                yield str(l_2_ip_address_secondary)
                yield ' secondary\n'
            l_2_ip_address_secondary = missing
        if (t_11(environment.getattr(l_1_ethernet_interface, 'ip_address'), 'dhcp') and t_11(environment.getattr(l_1_ethernet_interface, 'dhcp_client_accept_default_route'), True)):
            pass
            yield '   dhcp client accept default-route\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ip_verify_unicast_source_reachable_via')):
            pass
            yield '   ip verify unicast source reachable-via '
            yield str(environment.getattr(l_1_ethernet_interface, 'ip_verify_unicast_source_reachable_via'))
            yield '\n'
        if ((t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'interval')) and t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'min_rx'))) and t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'multiplier'))):
            pass
            yield '   bfd interval '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'interval'))
            yield ' min-rx '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'min_rx'))
            yield ' multiplier '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'multiplier'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'echo'), True):
            pass
            yield '   bfd echo\n'
        elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'bfd'), 'echo'), False):
            pass
            yield '   no bfd echo\n'
        for l_2_ip_helper in t_3(environment.getattr(l_1_ethernet_interface, 'ip_helpers'), 'ip_helper'):
            l_2_ip_helper_cli = missing
            _loop_vars = {}
            pass
            l_2_ip_helper_cli = str_join(('ip helper-address ', environment.getattr(l_2_ip_helper, 'ip_helper'), ))
            _loop_vars['ip_helper_cli'] = l_2_ip_helper_cli
            if t_11(environment.getattr(l_2_ip_helper, 'vrf')):
                pass
                l_2_ip_helper_cli = str_join(((undefined(name='ip_helper_cli') if l_2_ip_helper_cli is missing else l_2_ip_helper_cli), ' vrf ', environment.getattr(l_2_ip_helper, 'vrf'), ))
                _loop_vars['ip_helper_cli'] = l_2_ip_helper_cli
            if t_11(environment.getattr(l_2_ip_helper, 'source_interface')):
                pass
                l_2_ip_helper_cli = str_join(((undefined(name='ip_helper_cli') if l_2_ip_helper_cli is missing else l_2_ip_helper_cli), ' source-interface ', environment.getattr(l_2_ip_helper, 'source_interface'), ))
                _loop_vars['ip_helper_cli'] = l_2_ip_helper_cli
            yield '   '
            yield str((undefined(name='ip_helper_cli') if l_2_ip_helper_cli is missing else l_2_ip_helper_cli))
            yield '\n'
        l_2_ip_helper = l_2_ip_helper_cli = missing
        for l_2_destination in t_3(environment.getattr(l_1_ethernet_interface, 'ipv6_dhcp_relay_destinations'), 'address'):
            l_2_destination_cli = missing
            _loop_vars = {}
            pass
            l_2_destination_cli = str_join(('ipv6 dhcp relay destination ', environment.getattr(l_2_destination, 'address'), ))
            _loop_vars['destination_cli'] = l_2_destination_cli
            if t_11(environment.getattr(l_2_destination, 'vrf')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' vrf ', environment.getattr(l_2_destination, 'vrf'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            if t_11(environment.getattr(l_2_destination, 'local_interface')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' local-interface ', environment.getattr(l_2_destination, 'local_interface'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            elif t_11(environment.getattr(l_2_destination, 'source_address')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' source-address ', environment.getattr(l_2_destination, 'source_address'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            if t_11(environment.getattr(l_2_destination, 'link_address')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' link-address ', environment.getattr(l_2_destination, 'link_address'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            yield '   '
            yield str((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli))
            yield '\n'
        l_2_destination = l_2_destination_cli = missing
        if t_11(environment.getattr(l_1_ethernet_interface, 'dhcp_server_ipv4'), True):
            pass
            yield '   dhcp server ipv4\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'dhcp_server_ipv6'), True):
            pass
            yield '   dhcp server ipv6\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'enabled'), True):
            pass
            l_1_host_proxy_cli = 'ip igmp host-proxy'
            _loop_vars['host_proxy_cli'] = l_1_host_proxy_cli
            yield '   '
            yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
            yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'groups')):
                pass
                for l_2_proxy_group in environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'groups'):
                    _loop_vars = {}
                    pass
                    if (t_11(environment.getattr(l_2_proxy_group, 'exclude')) or t_11(environment.getattr(l_2_proxy_group, 'include'))):
                        pass
                        if t_11(environment.getattr(l_2_proxy_group, 'include')):
                            pass
                            for l_3_include_source in environment.getattr(l_2_proxy_group, 'include'):
                                _loop_vars = {}
                                pass
                                yield '   '
                                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                                yield ' '
                                yield str(environment.getattr(l_2_proxy_group, 'group'))
                                yield ' include '
                                yield str(environment.getattr(l_3_include_source, 'source'))
                                yield '\n'
                            l_3_include_source = missing
                        if t_11(environment.getattr(l_2_proxy_group, 'exclude')):
                            pass
                            for l_3_exclude_source in environment.getattr(l_2_proxy_group, 'exclude'):
                                _loop_vars = {}
                                pass
                                yield '   '
                                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                                yield ' '
                                yield str(environment.getattr(l_2_proxy_group, 'group'))
                                yield ' exclude '
                                yield str(environment.getattr(l_3_exclude_source, 'source'))
                                yield '\n'
                            l_3_exclude_source = missing
                    elif t_11(environment.getattr(l_2_proxy_group, 'group')):
                        pass
                        yield '   '
                        yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                        yield ' '
                        yield str(environment.getattr(l_2_proxy_group, 'group'))
                        yield '\n'
                l_2_proxy_group = missing
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'access_lists')):
                pass
                for l_2_access_list in environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'access_lists'):
                    _loop_vars = {}
                    pass
                    yield '   '
                    yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                    yield ' access-list '
                    yield str(environment.getattr(l_2_access_list, 'name'))
                    yield '\n'
                l_2_access_list = missing
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'report_interval')):
                pass
                yield '   '
                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                yield ' report-interval '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'report_interval'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'version')):
                pass
                yield '   '
                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                yield ' version '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_igmp_host_proxy'), 'version'))
                yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_enable'), True):
            pass
            yield '   ipv6 enable\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_address')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_ethernet_interface, 'ipv6_address'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_address_link_local')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_ethernet_interface, 'ipv6_address_link_local'))
            yield ' link-local\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_nd_ra_disabled'), True):
            pass
            yield '   ipv6 nd ra disabled\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_nd_managed_config_flag'), True):
            pass
            yield '   ipv6 nd managed-config-flag\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_nd_prefixes')):
            pass
            for l_2_prefix in environment.getattr(l_1_ethernet_interface, 'ipv6_nd_prefixes'):
                l_2_ipv6_nd_prefix_cli = missing
                _loop_vars = {}
                pass
                l_2_ipv6_nd_prefix_cli = str_join(('ipv6 nd prefix ', environment.getattr(l_2_prefix, 'ipv6_prefix'), ))
                _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                if t_11(environment.getattr(l_2_prefix, 'valid_lifetime')):
                    pass
                    l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' ', environment.getattr(l_2_prefix, 'valid_lifetime'), ))
                    _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                    if t_11(environment.getattr(l_2_prefix, 'preferred_lifetime')):
                        pass
                        l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' ', environment.getattr(l_2_prefix, 'preferred_lifetime'), ))
                        _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                if t_11(environment.getattr(l_2_prefix, 'no_autoconfig_flag'), True):
                    pass
                    l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' no-autoconfig', ))
                    _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                yield '   '
                yield str((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli))
                yield '\n'
            l_2_prefix = l_2_ipv6_nd_prefix_cli = missing
        if (t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'ipv4_segment_size')) or t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'ipv6_segment_size'))):
            pass
            l_1_tcp_mss_ceiling_cli = 'tcp mss ceiling'
            _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'ipv4_segment_size')):
                pass
                l_1_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli), ' ipv4 ', environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'ipv4_segment_size'), ))
                _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'ipv6_segment_size')):
                pass
                l_1_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli), ' ipv6 ', environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'ipv6_segment_size'), ))
                _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'direction')):
                pass
                l_1_tcp_mss_ceiling_cli = str_join(((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli), ' ', environment.getattr(environment.getattr(l_1_ethernet_interface, 'tcp_mss_ceiling'), 'direction'), ))
                _loop_vars['tcp_mss_ceiling_cli'] = l_1_tcp_mss_ceiling_cli
            yield '   '
            yield str((undefined(name='tcp_mss_ceiling_cli') if l_1_tcp_mss_ceiling_cli is missing else l_1_tcp_mss_ceiling_cli))
            yield '\n'
        if (t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id')) and t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'mode'))):
            pass
            yield '   channel-group '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'id'))
            yield ' mode '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'channel_group'), 'mode'))
            yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lacp_timer'), 'mode')):
                pass
                yield '   lacp timer '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lacp_timer'), 'mode'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lacp_timer'), 'multiplier')):
                pass
                yield '   lacp timer multiplier '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lacp_timer'), 'multiplier'))
                yield '\n'
            if t_11(environment.getattr(l_1_ethernet_interface, 'lacp_port_priority')):
                pass
                yield '   lacp port-priority '
                yield str(environment.getattr(l_1_ethernet_interface, 'lacp_port_priority'))
                yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'access_group_in')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_ethernet_interface, 'access_group_in'))
            yield ' in\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'access_group_out')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_ethernet_interface, 'access_group_out'))
            yield ' out\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_access_group_in')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_ethernet_interface, 'ipv6_access_group_in'))
            yield ' in\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ipv6_access_group_out')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_ethernet_interface, 'ipv6_access_group_out'))
            yield ' out\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'mac_access_group_in')):
            pass
            yield '   mac access-group '
            yield str(environment.getattr(l_1_ethernet_interface, 'mac_access_group_in'))
            yield ' in\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'mac_access_group_out')):
            pass
            yield '   mac access-group '
            yield str(environment.getattr(l_1_ethernet_interface, 'mac_access_group_out'))
            yield ' out\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mpls'), 'ldp'), 'igp_sync'), True):
            pass
            yield '   mpls ldp igp sync\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mpls'), 'ldp'), 'interface'), True):
            pass
            yield '   mpls ldp interface\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mpls'), 'ldp'), 'interface'), False):
            pass
            yield '   no mpls ldp interface\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lldp'), 'transmit'), False):
            pass
            yield '   no lldp transmit\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lldp'), 'receive'), False):
            pass
            yield '   no lldp receive\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lldp'), 'ztp_vlan')):
            pass
            yield '   lldp tlv transmit ztp vlan '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'lldp'), 'ztp_vlan'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mac_security'), 'profile')):
            pass
            yield '   mac security profile '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mac_security'), 'profile'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'multicast')):
            pass
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'multicast'), 'ipv4'), 'boundaries')):
                pass
                for l_2_boundary in environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'multicast'), 'ipv4'), 'boundaries'):
                    l_2_boundary_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_boundary_cli = str_join(('multicast ipv4 boundary ', environment.getattr(l_2_boundary, 'boundary'), ))
                    _loop_vars['boundary_cli'] = l_2_boundary_cli
                    if t_11(environment.getattr(l_2_boundary, 'out'), True):
                        pass
                        l_2_boundary_cli = str_join(((undefined(name='boundary_cli') if l_2_boundary_cli is missing else l_2_boundary_cli), ' out', ))
                        _loop_vars['boundary_cli'] = l_2_boundary_cli
                    yield '   '
                    yield str((undefined(name='boundary_cli') if l_2_boundary_cli is missing else l_2_boundary_cli))
                    yield '\n'
                l_2_boundary = l_2_boundary_cli = missing
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'multicast'), 'ipv6'), 'boundaries')):
                pass
                for l_2_boundary in environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'multicast'), 'ipv6'), 'boundaries'):
                    _loop_vars = {}
                    pass
                    yield '   multicast ipv6 boundary '
                    yield str(environment.getattr(l_2_boundary, 'boundary'))
                    yield ' out\n'
                l_2_boundary = missing
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'multicast'), 'ipv4'), 'static'), True):
                pass
                yield '   multicast ipv4 static\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'multicast'), 'ipv6'), 'static'), True):
                pass
                yield '   multicast ipv6 static\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mpls'), 'ip'), True):
            pass
            yield '   mpls ip\n'
        elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'mpls'), 'ip'), False):
            pass
            yield '   no mpls ip\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ip_nat')):
            pass
            l_1_interface_ip_nat = environment.getattr(l_1_ethernet_interface, 'ip_nat')
            _loop_vars['interface_ip_nat'] = l_1_interface_ip_nat
            template = environment.get_template('eos/interface-ip-nat.j2', 'eos/ethernet-interfaces.j2')
            gen = template.root_render_func(template.new_context(context.get_all(), True, {'aaa_config': l_1_aaa_config, 'actions': l_1_actions, 'address_locking_cli': l_1_address_locking_cli, 'auth_cli': l_1_auth_cli, 'auth_failure_fallback_mba': l_1_auth_failure_fallback_mba, 'backup_link_cli': l_1_backup_link_cli, 'both_key_ids': l_1_both_key_ids, 'client_encapsulation': l_1_client_encapsulation, 'dfe_algo_cli': l_1_dfe_algo_cli, 'dfe_hold_time_cli': l_1_dfe_hold_time_cli, 'encapsulation_cli': l_1_encapsulation_cli, 'encapsulation_dot1q_cli': l_1_encapsulation_dot1q_cli, 'ethernet_interface': l_1_ethernet_interface, 'frequency_cli': l_1_frequency_cli, 'host_mode_cli': l_1_host_mode_cli, 'host_proxy_cli': l_1_host_proxy_cli, 'interface_ip_nat': l_1_interface_ip_nat, 'isis_auth_cli': l_1_isis_auth_cli, 'network_encapsulation': l_1_network_encapsulation, 'network_flag': l_1_network_flag, 'poe_limit_cli': l_1_poe_limit_cli, 'poe_link_down_action_cli': l_1_poe_link_down_action_cli, 'sorted_vlans_cli': l_1_sorted_vlans_cli, 'tap_identity_cli': l_1_tap_identity_cli, 'tap_mac_address_cli': l_1_tap_mac_address_cli, 'tap_truncation_cli': l_1_tap_truncation_cli, 'tcp_mss_ceiling_cli': l_1_tcp_mss_ceiling_cli, 'tool_groups': l_1_tool_groups, 'POE_CLASS_MAP': l_0_POE_CLASS_MAP}))
            try:
                for event in gen:
                    yield event
            finally: gen.close()
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_nat'), 'service_profile')):
                pass
                yield '   ip nat service-profile '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ip_nat'), 'service_profile'))
                yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ospf_cost')):
            pass
            yield '   ip ospf cost '
            yield str(environment.getattr(l_1_ethernet_interface, 'ospf_cost'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ospf_network_point_to_point'), True):
            pass
            yield '   ip ospf network point-to-point\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ospf_authentication'), 'simple'):
            pass
            yield '   ip ospf authentication\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'ospf_authentication'), 'message-digest'):
            pass
            yield '   ip ospf authentication message-digest\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ospf_authentication_key')):
            pass
            yield '   ip ospf authentication-key 7 '
            yield str(t_2(environment.getattr(l_1_ethernet_interface, 'ospf_authentication_key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'ospf_area')):
            pass
            yield '   ip ospf area '
            yield str(environment.getattr(l_1_ethernet_interface, 'ospf_area'))
            yield '\n'
        for l_2_ospf_message_digest_key in t_3(environment.getattr(l_1_ethernet_interface, 'ospf_message_digest_keys'), 'id'):
            _loop_vars = {}
            pass
            if (t_11(environment.getattr(l_2_ospf_message_digest_key, 'hash_algorithm')) and t_11(environment.getattr(l_2_ospf_message_digest_key, 'key'))):
                pass
                yield '   ip ospf message-digest-key '
                yield str(environment.getattr(l_2_ospf_message_digest_key, 'id'))
                yield ' '
                yield str(environment.getattr(l_2_ospf_message_digest_key, 'hash_algorithm'))
                yield ' 7 '
                yield str(t_2(environment.getattr(l_2_ospf_message_digest_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
        l_2_ospf_message_digest_key = missing
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'service_policy'), 'pbr'), 'input')):
            pass
            yield '   service-policy type pbr input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'service_policy'), 'pbr'), 'input'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'sparse_mode'), True):
            pass
            yield '   pim ipv4 sparse-mode\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'bidirectional'), True):
            pass
            yield '   pim ipv4 bidirectional\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'border_router'), True):
            pass
            yield '   pim ipv4 border-router\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'hello'), 'interval')):
            pass
            yield '   pim ipv4 hello interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'hello'), 'interval'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'hello'), 'count')):
            pass
            yield '   pim ipv4 hello count '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'hello'), 'count'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'dr_priority')):
            pass
            yield '   pim ipv4 dr-priority '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'dr_priority'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'pim'), 'ipv4'), 'bfd'), True):
            pass
            yield '   pim ipv4 bfd\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'priority')):
            pass
            yield '   poe priority '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'priority'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'reboot'), 'action')):
            pass
            yield '   poe reboot action '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'reboot'), 'action'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'link_down'), 'action')):
            pass
            l_1_poe_link_down_action_cli = str_join(('poe link down action ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'link_down'), 'action'), ))
            _loop_vars['poe_link_down_action_cli'] = l_1_poe_link_down_action_cli
            if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'link_down'), 'power_off_delay')) and (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'link_down'), 'action') == 'power-off')):
                pass
                l_1_poe_link_down_action_cli = str_join(((undefined(name='poe_link_down_action_cli') if l_1_poe_link_down_action_cli is missing else l_1_poe_link_down_action_cli), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'link_down'), 'power_off_delay'), ' seconds', ))
                _loop_vars['poe_link_down_action_cli'] = l_1_poe_link_down_action_cli
            yield '   '
            yield str((undefined(name='poe_link_down_action_cli') if l_1_poe_link_down_action_cli is missing else l_1_poe_link_down_action_cli))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'shutdown'), 'action')):
            pass
            yield '   poe shutdown action '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'shutdown'), 'action'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'disabled'), True):
            pass
            yield '   poe disabled\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'limit')):
            pass
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'limit'), 'class')):
                pass
                l_1_poe_limit_cli = str_join(('poe limit ', environment.getitem((undefined(name='POE_CLASS_MAP') if l_0_POE_CLASS_MAP is missing else l_0_POE_CLASS_MAP), environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'limit'), 'class')), ' watts', ))
                _loop_vars['poe_limit_cli'] = l_1_poe_limit_cli
            elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'limit'), 'watts')):
                pass
                l_1_poe_limit_cli = str_join(('poe limit ', t_6('%.2f', t_5(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'limit'), 'watts'))), ' watts', ))
                _loop_vars['poe_limit_cli'] = l_1_poe_limit_cli
            if (t_11((undefined(name='poe_limit_cli') if l_1_poe_limit_cli is missing else l_1_poe_limit_cli)) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'limit'), 'fixed'), True)):
                pass
                l_1_poe_limit_cli = str_join(((undefined(name='poe_limit_cli') if l_1_poe_limit_cli is missing else l_1_poe_limit_cli), ' fixed', ))
                _loop_vars['poe_limit_cli'] = l_1_poe_limit_cli
            yield '   '
            yield str((undefined(name='poe_limit_cli') if l_1_poe_limit_cli is missing else l_1_poe_limit_cli))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'negotiation_lldp'), False):
            pass
            yield '   poe negotiation lldp disabled\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'poe'), 'legacy_detect'), True):
            pass
            yield '   poe legacy detect\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security')):
            pass
            if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'enabled'), True) or t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'violation'), 'mode'), 'shutdown')):
                pass
                yield '   switchport port-security\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'violation'), 'mode'), 'protect'):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'violation'), 'protect_log'), True):
                    pass
                    yield '   switchport port-security violation protect log\n'
                else:
                    pass
                    yield '   switchport port-security violation protect\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'disabled'), True):
                pass
                yield '   switchport port-security mac-address maximum disabled\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'disabled'), False):
                pass
                yield '   no switchport port-security mac-address maximum disabled\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'limit')):
                pass
                yield '   switchport port-security mac-address maximum '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'mac_address_maximum'), 'limit'))
                yield '\n'
            if (not t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'violation'), 'mode'), 'protect')):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'vlans')):
                    pass
                    l_1_sorted_vlans_cli = []
                    _loop_vars['sorted_vlans_cli'] = l_1_sorted_vlans_cli
                    for l_2_vlan in environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'vlans'):
                        _loop_vars = {}
                        pass
                        if (t_11(environment.getattr(l_2_vlan, 'range')) and t_11(environment.getattr(l_2_vlan, 'mac_address_maximum'))):
                            pass
                            for l_3_id in t_4(environment.getattr(l_2_vlan, 'range')):
                                l_3_port_sec_cli = missing
                                _loop_vars = {}
                                pass
                                l_3_port_sec_cli = str_join(('switchport port-security vlan ', l_3_id, ' mac-address maximum ', environment.getattr(l_2_vlan, 'mac_address_maximum'), ))
                                _loop_vars['port_sec_cli'] = l_3_port_sec_cli
                                context.call(environment.getattr((undefined(name='sorted_vlans_cli') if l_1_sorted_vlans_cli is missing else l_1_sorted_vlans_cli), 'append'), (undefined(name='port_sec_cli') if l_3_port_sec_cli is missing else l_3_port_sec_cli), _loop_vars=_loop_vars)
                            l_3_id = l_3_port_sec_cli = missing
                    l_2_vlan = missing
                    for l_2_vlan_cli in t_3((undefined(name='sorted_vlans_cli') if l_1_sorted_vlans_cli is missing else l_1_sorted_vlans_cli)):
                        _loop_vars = {}
                        pass
                        yield '   '
                        yield str(l_2_vlan_cli)
                        yield '\n'
                    l_2_vlan_cli = missing
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'vlan_default_mac_address_maximum')):
                    pass
                    yield '   switchport port-security vlan default mac-address maximum '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'port_security'), 'vlan_default_mac_address_maximum'))
                    yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'enable'), True):
            pass
            yield '   ptp enable\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'announce'), 'interval')):
            pass
            yield '   ptp announce interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'announce'), 'interval'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'announce'), 'timeout')):
            pass
            yield '   ptp announce timeout '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'announce'), 'timeout'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'delay_mechanism')):
            pass
            yield '   ptp delay-mechanism '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'delay_mechanism'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'delay_req')):
            pass
            yield '   ptp delay-req interval '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'delay_req'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'profile'), 'g8275_1'), 'destination_mac_address')):
            pass
            yield '   ptp profile g8275.1 destination mac-address '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'profile'), 'g8275_1'), 'destination_mac_address'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'role')):
            pass
            yield '   ptp role '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'role'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'sync_message'), 'interval')):
            pass
            yield '   ptp sync-message interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'sync_message'), 'interval'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'transport')):
            pass
            yield '   ptp transport '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'transport'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'vlan')):
            pass
            yield '   ptp vlan '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'ptp'), 'vlan'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'service_policy'), 'qos'), 'input')):
            pass
            yield '   service-policy type qos input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'service_policy'), 'qos'), 'input'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'service_profile')):
            pass
            yield '   service-profile '
            yield str(environment.getattr(l_1_ethernet_interface, 'service_profile'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'trust')):
            pass
            if (environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'trust') == 'disabled'):
                pass
                yield '   no qos trust\n'
            else:
                pass
                yield '   qos trust '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'trust'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'cos')):
            pass
            yield '   qos cos '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'cos'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'dscp')):
            pass
            yield '   qos dscp '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'qos'), 'dscp'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'shape'), 'rate')):
            pass
            yield '   shape rate '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'shape'), 'rate'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'priority_flow_control'), 'enabled'), True):
            pass
            yield '   priority-flow-control on\n'
        elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'priority_flow_control'), 'enabled'), False):
            pass
            yield '   no priority-flow-control\n'
        for l_2_priority_block in t_3(environment.getattr(environment.getattr(l_1_ethernet_interface, 'priority_flow_control'), 'priorities')):
            _loop_vars = {}
            pass
            if t_11(environment.getattr(l_2_priority_block, 'priority')):
                pass
                if t_11(environment.getattr(l_2_priority_block, 'no_drop'), True):
                    pass
                    yield '   priority-flow-control priority '
                    yield str(environment.getattr(l_2_priority_block, 'priority'))
                    yield ' no-drop\n'
                elif t_11(environment.getattr(l_2_priority_block, 'no_drop'), False):
                    pass
                    yield '   priority-flow-control priority '
                    yield str(environment.getattr(l_2_priority_block, 'priority'))
                    yield ' drop\n'
        l_2_priority_block = missing
        for l_2_tx_queue in t_3(environment.getattr(l_1_ethernet_interface, 'tx_queues'), 'id'):
            _loop_vars = {}
            pass
            template = environment.get_template('eos/ethernet-interface-tx-queues.j2', 'eos/ethernet-interfaces.j2')
            gen = template.root_render_func(template.new_context(context.get_all(), True, {'tx_queue': l_2_tx_queue, 'aaa_config': l_1_aaa_config, 'actions': l_1_actions, 'address_locking_cli': l_1_address_locking_cli, 'auth_cli': l_1_auth_cli, 'auth_failure_fallback_mba': l_1_auth_failure_fallback_mba, 'backup_link_cli': l_1_backup_link_cli, 'both_key_ids': l_1_both_key_ids, 'client_encapsulation': l_1_client_encapsulation, 'dfe_algo_cli': l_1_dfe_algo_cli, 'dfe_hold_time_cli': l_1_dfe_hold_time_cli, 'encapsulation_cli': l_1_encapsulation_cli, 'encapsulation_dot1q_cli': l_1_encapsulation_dot1q_cli, 'ethernet_interface': l_1_ethernet_interface, 'frequency_cli': l_1_frequency_cli, 'host_mode_cli': l_1_host_mode_cli, 'host_proxy_cli': l_1_host_proxy_cli, 'interface_ip_nat': l_1_interface_ip_nat, 'isis_auth_cli': l_1_isis_auth_cli, 'network_encapsulation': l_1_network_encapsulation, 'network_flag': l_1_network_flag, 'poe_limit_cli': l_1_poe_limit_cli, 'poe_link_down_action_cli': l_1_poe_link_down_action_cli, 'sorted_vlans_cli': l_1_sorted_vlans_cli, 'tap_identity_cli': l_1_tap_identity_cli, 'tap_mac_address_cli': l_1_tap_mac_address_cli, 'tap_truncation_cli': l_1_tap_truncation_cli, 'tcp_mss_ceiling_cli': l_1_tcp_mss_ceiling_cli, 'tool_groups': l_1_tool_groups, 'POE_CLASS_MAP': l_0_POE_CLASS_MAP}))
            try:
                for event in gen:
                    yield event
            finally: gen.close()
        l_2_tx_queue = missing
        for l_2_uc_tx_queue in t_3(environment.getattr(l_1_ethernet_interface, 'uc_tx_queues'), 'id'):
            _loop_vars = {}
            pass
            template = environment.get_template('eos/ethernet-interface-uc-tx-queues.j2', 'eos/ethernet-interfaces.j2')
            gen = template.root_render_func(template.new_context(context.get_all(), True, {'uc_tx_queue': l_2_uc_tx_queue, 'aaa_config': l_1_aaa_config, 'actions': l_1_actions, 'address_locking_cli': l_1_address_locking_cli, 'auth_cli': l_1_auth_cli, 'auth_failure_fallback_mba': l_1_auth_failure_fallback_mba, 'backup_link_cli': l_1_backup_link_cli, 'both_key_ids': l_1_both_key_ids, 'client_encapsulation': l_1_client_encapsulation, 'dfe_algo_cli': l_1_dfe_algo_cli, 'dfe_hold_time_cli': l_1_dfe_hold_time_cli, 'encapsulation_cli': l_1_encapsulation_cli, 'encapsulation_dot1q_cli': l_1_encapsulation_dot1q_cli, 'ethernet_interface': l_1_ethernet_interface, 'frequency_cli': l_1_frequency_cli, 'host_mode_cli': l_1_host_mode_cli, 'host_proxy_cli': l_1_host_proxy_cli, 'interface_ip_nat': l_1_interface_ip_nat, 'isis_auth_cli': l_1_isis_auth_cli, 'network_encapsulation': l_1_network_encapsulation, 'network_flag': l_1_network_flag, 'poe_limit_cli': l_1_poe_limit_cli, 'poe_link_down_action_cli': l_1_poe_link_down_action_cli, 'sorted_vlans_cli': l_1_sorted_vlans_cli, 'tap_identity_cli': l_1_tap_identity_cli, 'tap_mac_address_cli': l_1_tap_mac_address_cli, 'tap_truncation_cli': l_1_tap_truncation_cli, 'tcp_mss_ceiling_cli': l_1_tcp_mss_ceiling_cli, 'tool_groups': l_1_tool_groups, 'POE_CLASS_MAP': l_0_POE_CLASS_MAP}))
            try:
                for event in gen:
                    yield event
            finally: gen.close()
        l_2_uc_tx_queue = missing
        if t_11(environment.getattr(l_1_ethernet_interface, 'sflow')):
            pass
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sflow'), 'enable'), True):
                pass
                yield '   sflow enable\n'
            elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sflow'), 'enable'), False):
                pass
                yield '   no sflow enable\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sflow'), 'egress'), 'enable'), True):
                pass
                yield '   sflow egress enable\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sflow'), 'egress'), 'enable'), False):
                pass
                yield '   no sflow egress enable\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sflow'), 'egress'), 'unmodified_enable'), True):
                pass
                yield '   sflow egress unmodified enable\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sflow'), 'egress'), 'unmodified_enable'), False):
                pass
                yield '   no sflow egress unmodified enable\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_enable')):
            pass
            yield '   isis enable '
            yield str(environment.getattr(l_1_ethernet_interface, 'isis_enable'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_bfd'), True):
            pass
            yield '   isis bfd\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_circuit_type')):
            pass
            yield '   isis circuit-type '
            yield str(environment.getattr(l_1_ethernet_interface, 'isis_circuit_type'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_metric')):
            pass
            yield '   isis metric '
            yield str(environment.getattr(l_1_ethernet_interface, 'isis_metric'))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_passive'), True):
            pass
            yield '   isis passive\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_hello_padding'), False):
            pass
            yield '   no isis hello padding\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'isis_hello_padding'), True):
            pass
            yield '   isis hello padding\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_network_point_to_point'), True):
            pass
            yield '   isis network point-to-point\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'isis_authentication')):
            pass
            if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode') == 'sha') and t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'sha'), 'key_id')))) or ((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode') == 'shared-secret') and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'shared_secret'))))):
                pass
                l_1_isis_auth_cli = str_join(('isis authentication mode ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode'), ))
                _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                if (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode') == 'sha'):
                    pass
                    l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'sha'), 'key_id'), ))
                    _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                elif (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'mode') == 'shared-secret'):
                    pass
                    l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'shared_secret'), 'profile'), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'shared_secret'), 'algorithm'), ))
                    _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'rx_disabled'), True):
                    pass
                    l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' rx-disabled', ))
                    _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                yield '   '
                yield str((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli))
                yield '\n'
            else:
                pass
                if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode') == 'sha') and t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'sha'), 'key_id')))) or ((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode') == 'shared-secret') and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'shared_secret'))))):
                    pass
                    l_1_isis_auth_cli = str_join(('isis authentication mode ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode'), ))
                    _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    if (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode') == 'sha'):
                        pass
                        l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'sha'), 'key_id'), ))
                        _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    elif (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'mode') == 'shared-secret'):
                        pass
                        l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'shared_secret'), 'profile'), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'shared_secret'), 'algorithm'), ))
                        _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'rx_disabled'), True):
                        pass
                        l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' rx-disabled', ))
                        _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    yield '   '
                    yield str((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli))
                    yield ' level-1\n'
                if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode')) and (((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode') in ['md5', 'text']) or ((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode') == 'sha') and t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'sha'), 'key_id')))) or ((environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode') == 'shared-secret') and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'shared_secret'))))):
                    pass
                    l_1_isis_auth_cli = str_join(('isis authentication mode ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode'), ))
                    _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    if (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode') == 'sha'):
                        pass
                        l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' key-id ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'sha'), 'key_id'), ))
                        _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    elif (environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'mode') == 'shared-secret'):
                        pass
                        l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' profile ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'shared_secret'), 'profile'), ' algorithm ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'shared_secret'), 'algorithm'), ))
                        _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'rx_disabled'), True):
                        pass
                        l_1_isis_auth_cli = str_join(((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli), ' rx-disabled', ))
                        _loop_vars['isis_auth_cli'] = l_1_isis_auth_cli
                    yield '   '
                    yield str((undefined(name='isis_auth_cli') if l_1_isis_auth_cli is missing else l_1_isis_auth_cli))
                    yield ' level-2\n'
            l_1_both_key_ids = []
            _loop_vars['both_key_ids'] = l_1_both_key_ids
            for l_2_auth_key in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'key_ids'), 'id'):
                _loop_vars = {}
                pass
                context.call(environment.getattr((undefined(name='both_key_ids') if l_1_both_key_ids is missing else l_1_both_key_ids), 'append'), environment.getattr(l_2_auth_key, 'id'), _loop_vars=_loop_vars)
                if t_11(environment.getattr(l_2_auth_key, 'rfc_5310'), True):
                    pass
                    yield '   isis authentication key-id '
                    yield str(environment.getattr(l_2_auth_key, 'id'))
                    yield ' algorithm '
                    yield str(environment.getattr(l_2_auth_key, 'algorithm'))
                    yield ' rfc-5310 key '
                    yield str(environment.getattr(l_2_auth_key, 'key_type'))
                    yield ' '
                    yield str(t_2(environment.getattr(l_2_auth_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                    yield '\n'
                else:
                    pass
                    yield '   isis authentication key-id '
                    yield str(environment.getattr(l_2_auth_key, 'id'))
                    yield ' algorithm '
                    yield str(environment.getattr(l_2_auth_key, 'algorithm'))
                    yield ' key '
                    yield str(environment.getattr(l_2_auth_key, 'key_type'))
                    yield ' '
                    yield str(t_2(environment.getattr(l_2_auth_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                    yield '\n'
            l_2_auth_key = missing
            for l_2_auth_key in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'key_ids'), 'id'):
                _loop_vars = {}
                pass
                if (environment.getattr(l_2_auth_key, 'id') not in (undefined(name='both_key_ids') if l_1_both_key_ids is missing else l_1_both_key_ids)):
                    pass
                    if t_11(environment.getattr(l_2_auth_key, 'rfc_5310'), True):
                        pass
                        yield '   isis authentication key-id '
                        yield str(environment.getattr(l_2_auth_key, 'id'))
                        yield ' algorithm '
                        yield str(environment.getattr(l_2_auth_key, 'algorithm'))
                        yield ' rfc-5310 key '
                        yield str(environment.getattr(l_2_auth_key, 'key_type'))
                        yield ' '
                        yield str(t_2(environment.getattr(l_2_auth_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                        yield ' level-1\n'
                    else:
                        pass
                        yield '   isis authentication key-id '
                        yield str(environment.getattr(l_2_auth_key, 'id'))
                        yield ' algorithm '
                        yield str(environment.getattr(l_2_auth_key, 'algorithm'))
                        yield ' key '
                        yield str(environment.getattr(l_2_auth_key, 'key_type'))
                        yield ' '
                        yield str(t_2(environment.getattr(l_2_auth_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                        yield ' level-1\n'
            l_2_auth_key = missing
            for l_2_auth_key in t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'key_ids'), 'id'):
                _loop_vars = {}
                pass
                if (environment.getattr(l_2_auth_key, 'id') not in (undefined(name='both_key_ids') if l_1_both_key_ids is missing else l_1_both_key_ids)):
                    pass
                    if t_11(environment.getattr(l_2_auth_key, 'rfc_5310'), True):
                        pass
                        yield '   isis authentication key-id '
                        yield str(environment.getattr(l_2_auth_key, 'id'))
                        yield ' algorithm '
                        yield str(environment.getattr(l_2_auth_key, 'algorithm'))
                        yield ' rfc-5310 key '
                        yield str(environment.getattr(l_2_auth_key, 'key_type'))
                        yield ' '
                        yield str(t_2(environment.getattr(l_2_auth_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                        yield ' level-2\n'
                    else:
                        pass
                        yield '   isis authentication key-id '
                        yield str(environment.getattr(l_2_auth_key, 'id'))
                        yield ' algorithm '
                        yield str(environment.getattr(l_2_auth_key, 'algorithm'))
                        yield ' key '
                        yield str(environment.getattr(l_2_auth_key, 'key_type'))
                        yield ' '
                        yield str(t_2(environment.getattr(l_2_auth_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                        yield ' level-2\n'
            l_2_auth_key = missing
            if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'key_type')) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'key'))):
                pass
                yield '   isis authentication key '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'key_type'))
                yield ' '
                yield str(t_2(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'both'), 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            else:
                pass
                if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'key_type')) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'key'))):
                    pass
                    yield '   isis authentication key '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'key_type'))
                    yield ' '
                    yield str(t_2(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_1'), 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                    yield ' level-1\n'
                if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'key_type')) and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'key'))):
                    pass
                    yield '   isis authentication key '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'key_type'))
                    yield ' '
                    yield str(t_2(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'isis_authentication'), 'level_2'), 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                    yield ' level-2\n'
        else:
            pass
            if (t_11(environment.getattr(l_1_ethernet_interface, 'isis_authentication_mode')) and (environment.getattr(l_1_ethernet_interface, 'isis_authentication_mode') in ['text', 'md5'])):
                pass
                yield '   isis authentication mode '
                yield str(environment.getattr(l_1_ethernet_interface, 'isis_authentication_mode'))
                yield '\n'
            if t_11(environment.getattr(l_1_ethernet_interface, 'isis_authentication_key')):
                pass
                yield '   isis authentication key 7 '
                yield str(t_2(environment.getattr(l_1_ethernet_interface, 'isis_authentication_key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
        for l_2_section in t_3(environment.getattr(l_1_ethernet_interface, 'storm_control')):
            _loop_vars = {}
            pass
            if (t_11(environment.getattr(environment.getitem(environment.getattr(l_1_ethernet_interface, 'storm_control'), l_2_section), 'level')) and (l_2_section != 'all')):
                pass
                if t_11(environment.getattr(environment.getitem(environment.getattr(l_1_ethernet_interface, 'storm_control'), l_2_section), 'unit'), 'pps'):
                    pass
                    yield '   storm-control '
                    yield str(t_9(context.eval_ctx, l_2_section, '_', '-'))
                    yield ' level pps '
                    yield str(environment.getattr(environment.getitem(environment.getattr(l_1_ethernet_interface, 'storm_control'), l_2_section), 'level'))
                    yield '\n'
                else:
                    pass
                    yield '   storm-control '
                    yield str(t_9(context.eval_ctx, l_2_section, '_', '-'))
                    yield ' level '
                    yield str(environment.getattr(environment.getitem(environment.getattr(l_1_ethernet_interface, 'storm_control'), l_2_section), 'level'))
                    yield '\n'
        l_2_section = missing
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'storm_control'), 'all'), 'level')):
            pass
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'storm_control'), 'all'), 'unit'), 'pps'):
                pass
                yield '   storm-control all level pps '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'storm_control'), 'all'), 'level'))
                yield '\n'
            else:
                pass
                yield '   storm-control all level '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'storm_control'), 'all'), 'level'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'storm_control_discards'), True):
            pass
            yield '   logging event storm-control discards\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'storm_control_discards'), False):
            pass
            yield '   no logging event storm-control discards\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_portfast'), 'edge'):
            pass
            yield '   spanning-tree portfast\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_portfast'), 'network'):
            pass
            yield '   spanning-tree portfast network\n'
        if (t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_bpduguard')) and (environment.getattr(l_1_ethernet_interface, 'spanning_tree_bpduguard') in [True, 'True', 'enabled'])):
            pass
            yield '   spanning-tree bpduguard enable\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_bpduguard'), 'disabled'):
            pass
            yield '   spanning-tree bpduguard disable\n'
        if (t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_bpdufilter')) and (environment.getattr(l_1_ethernet_interface, 'spanning_tree_bpdufilter') in [True, 'True', 'enabled'])):
            pass
            yield '   spanning-tree bpdufilter enable\n'
        elif t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_bpdufilter'), 'disabled'):
            pass
            yield '   spanning-tree bpdufilter disable\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'spanning_tree_guard')):
            pass
            if (environment.getattr(l_1_ethernet_interface, 'spanning_tree_guard') == 'disabled'):
                pass
                yield '   spanning-tree guard none\n'
            else:
                pass
                yield '   spanning-tree guard '
                yield str(environment.getattr(l_1_ethernet_interface, 'spanning_tree_guard'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'spanning_tree'), True):
            pass
            yield '   logging event spanning-tree\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'logging'), 'event'), 'spanning_tree'), False):
            pass
            yield '   no logging event spanning-tree\n'
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup_link'), 'interface')):
            pass
            l_1_backup_link_cli = str_join(('switchport backup-link ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup_link'), 'interface'), ))
            _loop_vars['backup_link_cli'] = l_1_backup_link_cli
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup_link'), 'prefer_vlan')):
                pass
                l_1_backup_link_cli = str_join(((undefined(name='backup_link_cli') if l_1_backup_link_cli is missing else l_1_backup_link_cli), ' prefer vlan ', environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup_link'), 'prefer_vlan'), ))
                _loop_vars['backup_link_cli'] = l_1_backup_link_cli
            yield '   '
            yield str((undefined(name='backup_link_cli') if l_1_backup_link_cli is missing else l_1_backup_link_cli))
            yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'preemption_delay')):
                pass
                yield '   switchport backup preemption-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'preemption_delay'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'mac_move_burst')):
                pass
                yield '   switchport backup mac-move-burst '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'mac_move_burst'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'mac_move_burst_interval')):
                pass
                yield '   switchport backup mac-move-burst-interval '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'mac_move_burst_interval'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'initial_mac_move_delay')):
                pass
                yield '   switchport backup initial-mac-move-delay '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'initial_mac_move_delay'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'dest_macaddr')):
                pass
                yield '   switchport backup dest-macaddr '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'backup'), 'dest_macaddr'))
                yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sync_e'), 'enable'), True):
            pass
            yield '   !\n   sync-e\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sync_e'), 'priority')):
                pass
                yield '      priority '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'sync_e'), 'priority'))
                yield '\n'
        if (t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap')) or t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'))):
            pass
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'native_vlan')):
                pass
                yield '   switchport tap native vlan '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'native_vlan'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'identity'), 'id')):
                pass
                l_1_tap_identity_cli = str_join(('switchport tap identity ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'identity'), 'id'), ))
                _loop_vars['tap_identity_cli'] = l_1_tap_identity_cli
                if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'identity'), 'inner_vlan')):
                    pass
                    l_1_tap_identity_cli = str_join(((undefined(name='tap_identity_cli') if l_1_tap_identity_cli is missing else l_1_tap_identity_cli), ' inner ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'identity'), 'inner_vlan'), ))
                    _loop_vars['tap_identity_cli'] = l_1_tap_identity_cli
                yield '   '
                yield str((undefined(name='tap_identity_cli') if l_1_tap_identity_cli is missing else l_1_tap_identity_cli))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'mac_address'), 'destination')):
                pass
                l_1_tap_mac_address_cli = str_join(('switchport tap mac-address dest ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'mac_address'), 'destination'), ))
                _loop_vars['tap_mac_address_cli'] = l_1_tap_mac_address_cli
                if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'mac_address'), 'source')):
                    pass
                    l_1_tap_mac_address_cli = str_join(((undefined(name='tap_mac_address_cli') if l_1_tap_mac_address_cli is missing else l_1_tap_mac_address_cli), ' src ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'mac_address'), 'source'), ))
                    _loop_vars['tap_mac_address_cli'] = l_1_tap_mac_address_cli
                yield '   '
                yield str((undefined(name='tap_mac_address_cli') if l_1_tap_mac_address_cli is missing else l_1_tap_mac_address_cli))
                yield '\n'
            if (t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'encapsulation'), 'vxlan_strip'), True) and (not t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'mpls_pop_all'), True))):
                pass
                yield '   switchport tap encapsulation vxlan strip\n'
            for l_2_protocol in t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'encapsulation'), 'gre'), 'protocols'), 'protocol'):
                l_2_tap_encapsulation_cli = resolve('tap_encapsulation_cli')
                _loop_vars = {}
                pass
                if t_11(environment.getattr(l_2_protocol, 'strip'), True):
                    pass
                    l_2_tap_encapsulation_cli = str_join(('switchport tap encapsulation gre protocol ', environment.getattr(l_2_protocol, 'protocol'), ))
                    _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                    if t_11(environment.getattr(l_2_protocol, 'feature_header_length')):
                        pass
                        l_2_tap_encapsulation_cli = str_join(((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli), ' feature header length ', environment.getattr(l_2_protocol, 'feature_header_length'), ))
                        _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                    l_2_tap_encapsulation_cli = str_join(((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli), ' strip', ))
                    _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                    if t_11(environment.getattr(l_2_protocol, 're_encapsulation_ethernet_header'), True):
                        pass
                        l_2_tap_encapsulation_cli = str_join(((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli), ' re-encapsulation ethernet', ))
                        _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                    yield '   '
                    yield str((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli))
                    yield '\n'
            l_2_protocol = l_2_tap_encapsulation_cli = missing
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'encapsulation'), 'gre'), 'strip'), True):
                pass
                yield '   switchport tap encapsulation gre strip\n'
            for l_2_destination in t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'encapsulation'), 'gre'), 'destinations'), 'destination'):
                l_2_tap_encapsulation_cli = missing
                _loop_vars = {}
                pass
                l_2_tap_encapsulation_cli = str_join(('switchport tap encapsulation gre destination ', environment.getattr(l_2_destination, 'destination'), ))
                _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                if t_11(environment.getattr(l_2_destination, 'source')):
                    pass
                    l_2_tap_encapsulation_cli = str_join(((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli), ' source ', environment.getattr(l_2_destination, 'source'), ))
                    _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                for l_3_destination_protocol in t_3(environment.getattr(l_2_destination, 'protocols'), 'protocol'):
                    l_3_tap_encapsulation_protocol_cli = resolve('tap_encapsulation_protocol_cli')
                    _loop_vars = {}
                    pass
                    if t_11(environment.getattr(l_3_destination_protocol, 'strip'), True):
                        pass
                        l_3_tap_encapsulation_protocol_cli = str_join(((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli), ' protocol ', environment.getattr(l_3_destination_protocol, 'protocol'), ))
                        _loop_vars['tap_encapsulation_protocol_cli'] = l_3_tap_encapsulation_protocol_cli
                        if t_11(environment.getattr(l_3_destination_protocol, 'feature_header_length')):
                            pass
                            l_3_tap_encapsulation_protocol_cli = str_join(((undefined(name='tap_encapsulation_protocol_cli') if l_3_tap_encapsulation_protocol_cli is missing else l_3_tap_encapsulation_protocol_cli), ' feature header length ', environment.getattr(l_3_destination_protocol, 'feature_header_length'), ))
                            _loop_vars['tap_encapsulation_protocol_cli'] = l_3_tap_encapsulation_protocol_cli
                        l_3_tap_encapsulation_protocol_cli = str_join(((undefined(name='tap_encapsulation_protocol_cli') if l_3_tap_encapsulation_protocol_cli is missing else l_3_tap_encapsulation_protocol_cli), ' strip', ))
                        _loop_vars['tap_encapsulation_protocol_cli'] = l_3_tap_encapsulation_protocol_cli
                        if t_11(environment.getattr(l_3_destination_protocol, 're_encapsulation_ethernet_header'), True):
                            pass
                            l_3_tap_encapsulation_protocol_cli = str_join(((undefined(name='tap_encapsulation_protocol_cli') if l_3_tap_encapsulation_protocol_cli is missing else l_3_tap_encapsulation_protocol_cli), ' re-encapsulation ethernet', ))
                            _loop_vars['tap_encapsulation_protocol_cli'] = l_3_tap_encapsulation_protocol_cli
                        yield '   '
                        yield str((undefined(name='tap_encapsulation_protocol_cli') if l_3_tap_encapsulation_protocol_cli is missing else l_3_tap_encapsulation_protocol_cli))
                        yield '\n'
                l_3_destination_protocol = l_3_tap_encapsulation_protocol_cli = missing
                if t_11(environment.getattr(l_2_destination, 'strip'), True):
                    pass
                    l_2_tap_encapsulation_cli = str_join(((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli), ' strip', ))
                    _loop_vars['tap_encapsulation_cli'] = l_2_tap_encapsulation_cli
                    yield '   '
                    yield str((undefined(name='tap_encapsulation_cli') if l_2_tap_encapsulation_cli is missing else l_2_tap_encapsulation_cli))
                    yield '\n'
            l_2_destination = l_2_tap_encapsulation_cli = missing
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'mpls_pop_all'), True):
                pass
                yield '   switchport tap mpls pop all\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'mpls_pop_all'), True):
                pass
                yield '   switchport tool mpls pop all\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'encapsulation'), 'vn_tag_strip'), True):
                pass
                yield '   switchport tool encapsulation vn-tag strip\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'encapsulation'), 'dot1br_strip'), True):
                pass
                yield '   switchport tool encapsulation dot1br strip\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'allowed_vlan')):
                pass
                yield '   switchport tap allowed vlan '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'allowed_vlan'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'allowed_vlan')):
                pass
                yield '   switchport tool allowed vlan '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'allowed_vlan'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'identity'), 'tag')):
                pass
                yield '   switchport tool identity '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'identity'), 'tag'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'identity'), 'dot1q_dzgre_source')):
                pass
                yield '   switchport tool identity dot1q source dzgre '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'identity'), 'dot1q_dzgre_source'))
                yield '\n'
            elif t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'identity'), 'qinq_dzgre_source')):
                pass
                yield '   switchport tool identity qinq source dzgre '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'identity'), 'qinq_dzgre_source'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'truncation'), 'enabled'), True):
                pass
                l_1_tap_truncation_cli = 'switchport tap truncation'
                _loop_vars['tap_truncation_cli'] = l_1_tap_truncation_cli
                if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'truncation'), 'size')):
                    pass
                    l_1_tap_truncation_cli = str_join(((undefined(name='tap_truncation_cli') if l_1_tap_truncation_cli is missing else l_1_tap_truncation_cli), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'truncation'), 'size'), ))
                    _loop_vars['tap_truncation_cli'] = l_1_tap_truncation_cli
                yield '   '
                yield str((undefined(name='tap_truncation_cli') if l_1_tap_truncation_cli is missing else l_1_tap_truncation_cli))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'default'), 'groups')):
                pass
                yield '   switchport tap default group '
                yield str(t_8(context.eval_ctx, t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'default'), 'groups')), ' group '))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'default'), 'nexthop_groups')):
                pass
                yield '   switchport tap default nexthop-group '
                yield str(t_8(context.eval_ctx, t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'default'), 'nexthop_groups')), ' '))
                yield '\n'
            for l_2_interface in t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tap'), 'default'), 'interfaces')):
                _loop_vars = {}
                pass
                yield '   switchport tap default interface '
                yield str(l_2_interface)
                yield '\n'
            l_2_interface = missing
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'groups')):
                pass
                l_1_tool_groups = t_8(context.eval_ctx, t_3(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'groups')), ' ')
                _loop_vars['tool_groups'] = l_1_tool_groups
                yield '   switchport tool group set '
                yield str((undefined(name='tool_groups') if l_1_tool_groups is missing else l_1_tool_groups))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'dot1q_remove_outer_vlan_tag')):
                pass
                yield '   switchport tool dot1q remove outer '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'dot1q_remove_outer_vlan_tag'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'switchport'), 'tool'), 'dzgre_preserve'), True):
                pass
                yield '   switchport tool dzgre preserve\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'enabled'), True):
            pass
            yield '   traffic-engineering\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'bandwidth')):
            pass
            yield '   traffic-engineering bandwidth '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'bandwidth'), 'number'))
            yield ' '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'bandwidth'), 'unit'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'administrative_groups')):
            pass
            yield '   traffic-engineering administrative-group '
            yield str(t_8(context.eval_ctx, environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'administrative_groups'), ','))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'srlg')):
            pass
            yield '   traffic-engineering srlg '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'srlg'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'metric')):
            pass
            yield '   traffic-engineering metric '
            yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'metric'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'min_delay_static')):
            pass
            yield '   traffic-engineering min-delay static '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'min_delay_static'), 'number'))
            yield ' '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'min_delay_static'), 'unit'))
            yield '\n'
        elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'min_delay_dynamic'), 'twamp_light_fallback')):
            pass
            yield '   traffic-engineering min-delay dynamic twamp-light fallback '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'min_delay_dynamic'), 'twamp_light_fallback'), 'number'))
            yield ' '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'traffic_engineering'), 'min_delay_dynamic'), 'twamp_light_fallback'), 'unit'))
            yield '\n'
        for l_2_link_tracking_group in t_3(environment.getattr(l_1_ethernet_interface, 'link_tracking_groups')):
            _loop_vars = {}
            pass
            if (t_11(environment.getattr(l_2_link_tracking_group, 'name')) and t_11(environment.getattr(l_2_link_tracking_group, 'direction'))):
                pass
                yield '   link tracking group '
                yield str(environment.getattr(l_2_link_tracking_group, 'name'))
                yield ' '
                yield str(environment.getattr(l_2_link_tracking_group, 'direction'))
                yield '\n'
        l_2_link_tracking_group = missing
        if (t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'link_tracking'), 'direction')) and t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'link_tracking'), 'groups'))):
            pass
            for l_2_group_name in environment.getattr(environment.getattr(l_1_ethernet_interface, 'link_tracking'), 'groups'):
                _loop_vars = {}
                pass
                yield '   link tracking group '
                yield str(l_2_group_name)
                yield ' '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'link_tracking'), 'direction'))
                yield '\n'
            l_2_group_name = missing
        if t_11(environment.getattr(l_1_ethernet_interface, 'vmtracer'), True):
            pass
            yield '   vmtracer vmware-esx\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'vrrp_ids')):
            pass
            def t_12(fiter):
                for l_2_vrid in fiter:
                    if t_11(environment.getattr(l_2_vrid, 'id')):
                        yield l_2_vrid
            for l_2_vrid in t_12(t_3(environment.getattr(l_1_ethernet_interface, 'vrrp_ids'), 'id')):
                l_2_delay_cli = resolve('delay_cli')
                _loop_vars = {}
                pass
                if t_11(environment.getattr(l_2_vrid, 'priority_level')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' priority-level '
                    yield str(environment.getattr(l_2_vrid, 'priority_level'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(l_2_vrid, 'advertisement'), 'interval')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' advertisement interval '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'advertisement'), 'interval'))
                    yield '\n'
                if (t_11(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'enabled'), True) and (t_11(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'minimum')) or t_11(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'reload')))):
                    pass
                    l_2_delay_cli = str_join(('vrrp ', environment.getattr(l_2_vrid, 'id'), ' preempt delay', ))
                    _loop_vars['delay_cli'] = l_2_delay_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'minimum')):
                        pass
                        l_2_delay_cli = str_join(((undefined(name='delay_cli') if l_2_delay_cli is missing else l_2_delay_cli), ' minimum ', environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'minimum'), ))
                        _loop_vars['delay_cli'] = l_2_delay_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'reload')):
                        pass
                        l_2_delay_cli = str_join(((undefined(name='delay_cli') if l_2_delay_cli is missing else l_2_delay_cli), ' reload ', environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'reload'), ))
                        _loop_vars['delay_cli'] = l_2_delay_cli
                    yield '   '
                    yield str((undefined(name='delay_cli') if l_2_delay_cli is missing else l_2_delay_cli))
                    yield '\n'
                elif t_11(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'enabled'), False):
                    pass
                    yield '   no vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' preempt\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'timers'), 'delay'), 'reload')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' timers delay reload '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'timers'), 'delay'), 'reload'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'address')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' ipv4 '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'address'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'version')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' ipv4 version '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'version'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(l_2_vrid, 'ipv6'), 'address')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' ipv6 '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'ipv6'), 'address'))
                    yield '\n'
                for l_3_tracked_obj in t_3(environment.getattr(l_2_vrid, 'tracked_object'), 'name'):
                    l_3_tracked_obj_cli = resolve('tracked_obj_cli')
                    _loop_vars = {}
                    pass
                    if t_11(environment.getattr(l_3_tracked_obj, 'name')):
                        pass
                        l_3_tracked_obj_cli = str_join(('vrrp ', environment.getattr(l_2_vrid, 'id'), ' tracked-object ', environment.getattr(l_3_tracked_obj, 'name'), ))
                        _loop_vars['tracked_obj_cli'] = l_3_tracked_obj_cli
                        if t_11(environment.getattr(l_3_tracked_obj, 'decrement')):
                            pass
                            l_3_tracked_obj_cli = str_join(((undefined(name='tracked_obj_cli') if l_3_tracked_obj_cli is missing else l_3_tracked_obj_cli), ' decrement ', environment.getattr(l_3_tracked_obj, 'decrement'), ))
                            _loop_vars['tracked_obj_cli'] = l_3_tracked_obj_cli
                        elif t_11(environment.getattr(l_3_tracked_obj, 'shutdown'), True):
                            pass
                            l_3_tracked_obj_cli = str_join(((undefined(name='tracked_obj_cli') if l_3_tracked_obj_cli is missing else l_3_tracked_obj_cli), ' shutdown', ))
                            _loop_vars['tracked_obj_cli'] = l_3_tracked_obj_cli
                        yield '   '
                        yield str((undefined(name='tracked_obj_cli') if l_3_tracked_obj_cli is missing else l_3_tracked_obj_cli))
                        yield '\n'
                l_3_tracked_obj = l_3_tracked_obj_cli = missing
            l_2_vrid = l_2_delay_cli = missing
        if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'transceiver'), 'media'), 'override')):
            pass
            yield '   transceiver media override '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'transceiver'), 'media'), 'override'))
            yield '\n'
        if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'transceiver'), 'frequency')):
            pass
            l_1_frequency_cli = str_join(('transceiver frequency ', t_6('%.3f', t_5(environment.getattr(environment.getattr(l_1_ethernet_interface, 'transceiver'), 'frequency'))), ))
            _loop_vars['frequency_cli'] = l_1_frequency_cli
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'transceiver'), 'frequency_unit')):
                pass
                l_1_frequency_cli = str_join(((undefined(name='frequency_cli') if l_1_frequency_cli is missing else l_1_frequency_cli), ' ', environment.getattr(environment.getattr(l_1_ethernet_interface, 'transceiver'), 'frequency_unit'), ))
                _loop_vars['frequency_cli'] = l_1_frequency_cli
            yield '   '
            yield str((undefined(name='frequency_cli') if l_1_frequency_cli is missing else l_1_frequency_cli))
            yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'dot1x')):
            pass
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'pae'), 'mode')):
                pass
                yield '   dot1x pae '
                yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'pae'), 'mode'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'authentication_failure')):
                pass
                if (t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'authentication_failure'), 'action'), 'allow') and t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'authentication_failure'), 'allow_vlan'))):
                    pass
                    yield '   dot1x authentication failure action traffic allow vlan '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'authentication_failure'), 'allow_vlan'))
                    yield '\n'
                elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'authentication_failure'), 'action'), 'drop'):
                    pass
                    yield '   dot1x authentication failure action traffic drop\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'aaa'), 'unresponsive')):
                pass
                l_1_aaa_config = 'dot1x aaa unresponsive'
                _loop_vars['aaa_config'] = l_1_aaa_config
                l_1_actions = environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'aaa'), 'unresponsive')
                _loop_vars['actions'] = l_1_actions
                for l_2_action in t_10(environment, (undefined(name='actions') if l_1_actions is missing else l_1_actions), reverse=True):
                    l_2_aaa_action_config = resolve('aaa_action_config')
                    l_2_action_apply_config = resolve('action_apply_config')
                    _loop_vars = {}
                    pass
                    if (l_2_action == 'phone_action'):
                        pass
                        l_2_aaa_action_config = str_join(((undefined(name='aaa_config') if l_1_aaa_config is missing else l_1_aaa_config), ' phone action', ))
                        _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                    elif (l_2_action == 'action'):
                        pass
                        l_2_aaa_action_config = str_join(((undefined(name='aaa_config') if l_1_aaa_config is missing else l_1_aaa_config), ' action', ))
                        _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                    if t_11((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config)):
                        pass
                        if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'apply_cached_results'), True):
                            pass
                            l_2_action_apply_config = 'apply cached-results'
                            _loop_vars['action_apply_config'] = l_2_action_apply_config
                            if (t_11(environment.getattr(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'cached_results_timeout'), 'time_duration')) and t_11(environment.getattr(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'cached_results_timeout'), 'time_duration_unit'))):
                                pass
                                l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' ', (undefined(name='action_apply_config') if l_2_action_apply_config is missing else l_2_action_apply_config), ' timeout ', environment.getattr(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'cached_results_timeout'), 'time_duration'), ' ', environment.getattr(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'cached_results_timeout'), 'time_duration_unit'), ))
                                _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                        if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow'), True):
                            pass
                            if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'apply_alternate'), True):
                                pass
                                l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' else traffic allow', ))
                                _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                            else:
                                pass
                                l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' traffic allow', ))
                                _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                        else:
                            pass
                            if (t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_vlan')) and t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_access_list'))):
                                pass
                                if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'apply_alternate'), True):
                                    pass
                                    l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' else traffic allow vlan ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_vlan'), ' access-list ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_access_list'), ))
                                    _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                                else:
                                    pass
                                    l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' traffic allow vlan ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_vlan'), ' access-list ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_access_list'), ))
                                    _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                            else:
                                pass
                                if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_vlan')):
                                    pass
                                    if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'apply_alternate'), True):
                                        pass
                                        l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' else traffic allow vlan ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_vlan'), ))
                                        _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                                    else:
                                        pass
                                        l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' traffic allow vlan ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_vlan'), ))
                                        _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                                if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_access_list')):
                                    pass
                                    if t_11(environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'apply_alternate'), True):
                                        pass
                                        l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' else traffic allow access list ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_access_list'), ))
                                        _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                                    else:
                                        pass
                                        l_2_aaa_action_config = str_join(((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config), ' traffic allow access list ', environment.getattr(environment.getitem((undefined(name='actions') if l_1_actions is missing else l_1_actions), l_2_action), 'traffic_allow_access_list'), ))
                                        _loop_vars['aaa_action_config'] = l_2_aaa_action_config
                        yield '   '
                        yield str((undefined(name='aaa_action_config') if l_2_aaa_action_config is missing else l_2_aaa_action_config))
                        yield '\n'
                l_2_action = l_2_aaa_action_config = l_2_action_apply_config = missing
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'aaa'), 'unresponsive'), 'eap_response')):
                pass
                yield '   '
                yield str((undefined(name='aaa_config') if l_1_aaa_config is missing else l_1_aaa_config))
                yield ' eap response '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'aaa'), 'unresponsive'), 'eap_response'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'reauthentication'), True):
                pass
                yield '   dot1x reauthentication\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'port_control')):
                pass
                yield '   dot1x port-control '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'port_control'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'port_control_force_authorized_phone'), True):
                pass
                yield '   dot1x port-control force-authorized phone\n'
            elif t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'port_control_force_authorized_phone'), False):
                pass
                yield '   no dot1x port-control force-authorized phone\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'host_mode')):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'host_mode'), 'mode'), 'single-host'):
                    pass
                    yield '   dot1x host-mode single-host\n'
                elif t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'host_mode'), 'mode'), 'multi-host'):
                    pass
                    l_1_host_mode_cli = 'dot1x host-mode multi-host'
                    _loop_vars['host_mode_cli'] = l_1_host_mode_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'host_mode'), 'multi_host_authenticated'), True):
                        pass
                        l_1_host_mode_cli = str_join(((undefined(name='host_mode_cli') if l_1_host_mode_cli is missing else l_1_host_mode_cli), ' authenticated', ))
                        _loop_vars['host_mode_cli'] = l_1_host_mode_cli
                    yield '   '
                    yield str((undefined(name='host_mode_cli') if l_1_host_mode_cli is missing else l_1_host_mode_cli))
                    yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'eapol'), 'disabled'), True):
                pass
                yield '   dot1x eapol disabled\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'mac_based_access_list'), True):
                pass
                yield '   dot1x mac based access-list\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'mac_based_authentication'), 'enabled'), True):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'mac_based_authentication'), 'host_mode_common'), True):
                    pass
                    yield '   dot1x mac based authentication host-mode common\n'
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'mac_based_authentication'), 'always'), True):
                        pass
                        yield '   dot1x mac based authentication always\n'
                else:
                    pass
                    l_1_auth_cli = 'dot1x mac based authentication'
                    _loop_vars['auth_cli'] = l_1_auth_cli
                    if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'mac_based_authentication'), 'always'), True):
                        pass
                        l_1_auth_cli = str_join(((undefined(name='auth_cli') if l_1_auth_cli is missing else l_1_auth_cli), ' always', ))
                        _loop_vars['auth_cli'] = l_1_auth_cli
                    yield '   '
                    yield str((undefined(name='auth_cli') if l_1_auth_cli is missing else l_1_auth_cli))
                    yield '\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout')):
                pass
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'quiet_period')):
                    pass
                    yield '   dot1x timeout quiet-period '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'quiet_period'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'reauth_timeout_ignore'), True):
                    pass
                    yield '   dot1x timeout reauth-timeout-ignore always\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'tx_period')):
                    pass
                    yield '   dot1x timeout tx-period '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'tx_period'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'reauth_period')):
                    pass
                    yield '   dot1x timeout reauth-period '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'reauth_period'))
                    yield '\n'
                if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'idle_host')):
                    pass
                    yield '   dot1x timeout idle-host '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'timeout'), 'idle_host'))
                    yield ' seconds\n'
            if t_11(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'reauthorization_request_limit')):
                pass
                yield '   dot1x reauthorization request limit '
                yield str(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'reauthorization_request_limit'))
                yield '\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'unauthorized'), 'access_vlan_membership_egress'), True):
                pass
                yield '   dot1x unauthorized access vlan membership egress\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'unauthorized'), 'native_vlan_membership_egress'), True):
                pass
                yield '   dot1x unauthorized native vlan membership egress\n'
            if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'eapol'), 'authentication_failure_fallback_mba'), 'enabled'), True):
                pass
                l_1_auth_failure_fallback_mba = 'dot1x eapol authentication failure fallback mba'
                _loop_vars['auth_failure_fallback_mba'] = l_1_auth_failure_fallback_mba
                if t_11(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'eapol'), 'authentication_failure_fallback_mba'), 'timeout')):
                    pass
                    l_1_auth_failure_fallback_mba = str_join(((undefined(name='auth_failure_fallback_mba') if l_1_auth_failure_fallback_mba is missing else l_1_auth_failure_fallback_mba), ' timeout ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_ethernet_interface, 'dot1x'), 'eapol'), 'authentication_failure_fallback_mba'), 'timeout'), ))
                    _loop_vars['auth_failure_fallback_mba'] = l_1_auth_failure_fallback_mba
                yield '   '
                yield str((undefined(name='auth_failure_fallback_mba') if l_1_auth_failure_fallback_mba is missing else l_1_auth_failure_fallback_mba))
                yield '\n'
        if t_11(environment.getattr(l_1_ethernet_interface, 'eos_cli')):
            pass
            yield '   '
            yield str(t_7(environment.getattr(l_1_ethernet_interface, 'eos_cli'), 3, False))
            yield '\n'
    l_1_ethernet_interface = l_1_encapsulation_cli = l_1_encapsulation_dot1q_cli = l_1_client_encapsulation = l_1_network_flag = l_1_network_encapsulation = l_1_dfe_algo_cli = l_1_dfe_hold_time_cli = l_1_address_locking_cli = l_1_host_proxy_cli = l_1_tcp_mss_ceiling_cli = l_1_interface_ip_nat = l_1_hide_passwords = l_1_poe_link_down_action_cli = l_1_poe_limit_cli = l_1_sorted_vlans_cli = l_1_isis_auth_cli = l_1_both_key_ids = l_1_backup_link_cli = l_1_tap_identity_cli = l_1_tap_mac_address_cli = l_1_tap_truncation_cli = l_1_tool_groups = l_1_frequency_cli = l_1_aaa_config = l_1_actions = l_1_host_mode_cli = l_1_auth_cli = l_1_auth_failure_fallback_mba = missing

blocks = {}
debug_info = '7=79&8=82&10=114&11=116&12=118&13=122&16=125&17=128&19=130&20=133&22=135&23=138&25=140&26=143&28=145&30=148&33=151&34=154&36=156&37=159&39=161&41=164&44=167&45=170&47=172&48=175&50=177&51=180&53=182&54=185&56=187&57=190&59=192&61=195&64=198&65=201&67=203&70=208&72=211&75=214&77=217&81=220&82=222&83=225&86=227&87=230&89=232&90=234&92=237&93=240&96=242&97=245&99=247&100=250&102=252&104=255&105=258&107=260&108=263&110=265&111=268&113=270&116=273&119=276&120=279&122=281&123=283&124=286&127=288&128=291&130=293&131=296&133=298&134=301&136=303&137=306&139=308&142=311&143=315&145=318&146=322&148=325&150=328&151=330&153=333&155=335&156=338&157=340&158=342&159=344&160=346&161=348&162=350&164=352&165=354&166=356&167=358&168=360&169=362&171=364&172=366&174=368&176=371&178=373&181=376&183=379&186=382&187=384&188=386&189=388&191=391&193=393&194=396&196=398&197=400&198=402&199=404&200=406&201=408&202=410&203=412&204=414&206=418&208=420&209=422&210=424&213=426&214=428&216=430&217=432&218=434&219=436&220=438&221=440&222=442&223=444&224=446&226=450&229=452&230=454&231=456&232=458&236=461&239=463&240=466&242=468&243=472&244=474&245=476&246=478&248=480&249=482&250=485&253=488&254=492&255=494&256=496&257=498&258=500&259=502&260=504&263=506&264=509&266=512&267=514&268=518&269=520&270=522&271=524&272=526&274=528&275=531&278=534&279=536&280=540&281=542&282=544&283=546&284=548&285=550&288=552&289=555&293=558&295=561&298=564&301=567&302=570&304=572&305=575&307=577&308=580&310=582&311=585&313=587&316=590&317=593&319=595&320=598&322=600&323=602&325=605&326=607&327=609&328=611&330=614&332=616&333=618&334=620&335=622&337=625&339=627&341=630&345=633&346=636&348=638&349=641&351=643&352=646&355=648&356=651&358=653&359=656&361=658&363=661&366=664&369=667&372=670&375=673&378=676&381=679&384=682&385=684&386=686&387=688&389=690&390=692&392=695&394=697&395=700&397=702&400=705&401=708&402=710&403=714&406=717&409=720&410=723&412=725&415=728&417=734&419=737&422=740&423=744&424=746&425=748&427=750&428=752&430=755&432=758&433=762&434=764&435=766&437=768&438=770&439=772&440=774&442=776&443=778&445=781&447=784&450=787&453=790&454=792&455=795&456=797&457=799&458=802&459=804&460=806&461=810&464=817&465=819&466=823&469=830&470=833&474=838&475=840&476=844&479=849&480=852&482=856&483=859&486=863&489=866&490=869&492=871&493=874&495=876&498=879&501=882&502=884&503=888&504=890&505=892&506=894&507=896&510=898&511=900&513=903&516=906&517=908&518=910&519=912&521=914&522=916&524=918&525=920&527=923&529=925&530=928&531=932&532=935&534=937&535=940&537=942&538=945&541=947&542=950&544=952&545=955&547=957&548=960&550=962&551=965&553=967&554=970&556=972&557=975&559=977&562=980&564=983&567=986&570=989&573=992&574=995&576=997&577=1000&579=1002&580=1004&581=1006&582=1010&583=1012&584=1014&586=1017&589=1020&590=1022&591=1026&594=1029&597=1032&601=1035&603=1038&606=1041&607=1043&608=1045&609=1051&610=1054&613=1056&614=1059&616=1061&619=1064&621=1067&624=1070&625=1073&627=1075&628=1078&630=1080&631=1083&632=1086&635=1093&636=1096&638=1098&641=1101&644=1104&647=1107&648=1110&650=1112&651=1115&653=1117&654=1120&656=1122&659=1125&660=1128&662=1130&663=1133&665=1135&666=1137&667=1139&668=1141&670=1144&672=1146&673=1149&675=1151&678=1154&679=1156&680=1158&681=1160&682=1162&684=1164&685=1166&687=1169&689=1171&692=1174&695=1177&696=1179&698=1182&699=1184&705=1190&707=1193&709=1196&710=1199&712=1201&713=1203&714=1205&715=1207&716=1210&717=1212&718=1216&719=1218&723=1221&724=1225&727=1228&728=1231&732=1233&735=1236&736=1239&738=1241&739=1244&741=1246&742=1249&744=1251&745=1254&747=1256&748=1259&750=1261&751=1264&753=1266&754=1269&756=1271&757=1274&759=1276&760=1279&762=1281&763=1284&765=1286&766=1289&768=1291&769=1293&772=1299&775=1301&776=1304&778=1306&779=1309&781=1311&782=1314&784=1316&786=1319&789=1322&790=1325&791=1327&792=1330&793=1332&794=1335&798=1338&799=1341&801=1348&802=1351&804=1358&805=1360&807=1363&810=1366&812=1369&815=1372&817=1375&821=1378&822=1381&824=1383&827=1386&828=1389&830=1391&831=1394&833=1396&836=1399&838=1402&841=1405&844=1408&845=1410&849=1412&850=1414&851=1416&852=1418&853=1420&855=1422&856=1424&858=1427&860=1431&865=1433&866=1435&867=1437&868=1439&869=1441&871=1443&872=1445&874=1448&876=1450&881=1452&882=1454&883=1456&884=1458&885=1460&887=1462&888=1464&890=1467&893=1469&894=1471&895=1474&896=1475&897=1478&899=1489&902=1498&903=1501&904=1503&905=1506&907=1517&911=1526&912=1529&913=1531&914=1534&916=1545&920=1554&921=1557&923=1563&924=1566&926=1570&927=1573&931=1579&933=1582&935=1584&936=1587&939=1589&940=1592&941=1594&942=1597&944=1604&948=1609&949=1611&950=1614&952=1619&955=1621&957=1624&960=1627&962=1630&965=1633&967=1636&970=1639&972=1642&975=1645&976=1647&979=1653&982=1655&984=1658&987=1661&988=1663&989=1665&990=1667&992=1670&993=1672&994=1675&996=1677&997=1680&999=1682&1000=1685&1002=1687&1003=1690&1005=1692&1006=1695&1009=1697&1012=1700&1013=1703&1016=1705&1017=1707&1018=1710&1020=1712&1021=1714&1022=1716&1023=1718&1025=1721&1027=1723&1028=1725&1029=1727&1030=1729&1032=1732&1034=1734&1037=1737&1038=1741&1039=1743&1040=1745&1041=1747&1043=1749&1044=1751&1045=1753&1047=1756&1050=1759&1053=1762&1054=1766&1055=1768&1056=1770&1058=1772&1059=1776&1060=1778&1061=1780&1062=1782&1064=1784&1065=1786&1066=1788&1068=1791&1071=1794&1072=1796&1073=1799&1076=1802&1079=1805&1082=1808&1085=1811&1088=1814&1089=1817&1091=1819&1092=1822&1094=1824&1095=1827&1097=1829&1098=1832&1099=1834&1100=1837&1102=1839&1103=1841&1104=1843&1105=1845&1107=1848&1109=1850&1110=1853&1112=1855&1113=1858&1115=1860&1116=1864&1118=1867&1119=1869&1120=1872&1122=1874&1123=1877&1125=1879&1129=1882&1132=1885&1133=1888&1135=1892&1136=1895&1138=1897&1139=1900&1141=1902&1142=1905&1144=1907&1145=1910&1146=1914&1147=1917&1149=1921&1150=1924&1151=1927&1154=1932&1155=1934&1156=1938&1159=1943&1162=1946&1163=1948&1164=1956&1165=1959&1167=1963&1168=1966&1170=1970&1173=1972&1174=1974&1175=1976&1177=1978&1178=1980&1180=1983&1181=1985&1182=1988&1184=1990&1185=1993&1187=1997&1188=2000&1190=2004&1191=2007&1193=2011&1194=2014&1196=2018&1197=2022&1198=2024&1199=2026&1200=2028&1201=2030&1202=2032&1204=2035&1209=2039&1210=2042&1212=2044&1213=2046&1214=2048&1215=2050&1217=2053&1219=2055&1220=2057&1221=2060&1223=2062&1224=2064&1226=2067&1227=2069&1231=2072&1232=2074&1233=2076&1234=2078&1235=2083&1236=2085&1237=2087&1238=2089&1240=2091&1241=2093&1242=2095&1243=2097&1244=2099&1247=2101&1248=2103&1249=2105&1251=2109&1254=2113&1255=2115&1256=2117&1258=2121&1261=2125&1262=2127&1263=2129&1265=2133&1268=2135&1269=2137&1270=2139&1272=2143&1277=2146&1281=2149&1282=2152&1284=2156&1287=2159&1288=2162&1290=2164&1292=2167&1295=2170&1296=2172&1298=2175&1299=2177&1300=2179&1301=2181&1303=2184&1306=2186&1309=2189&1312=2192&1313=2194&1315=2197&1319=2202&1320=2204&1321=2206&1323=2209&1326=2211&1327=2213&1328=2216&1330=2218&1333=2221&1334=2224&1336=2226&1337=2229&1339=2231&1340=2234&1343=2236&1344=2239&1346=2241&1349=2244&1352=2247&1353=2249&1354=2251&1355=2253&1357=2256&1360=2258&1361=2261'