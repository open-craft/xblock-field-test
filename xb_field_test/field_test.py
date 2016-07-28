# -*- coding: utf-8 -*-
"""
FieldTestXBlock: XBlock to test XBlock field scopes
"""

from __future__ import unicode_literals

import jinja2
from xblock import fields
from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError, InvalidScopeError
from xblock.fields import BlockScope, UserScope, Scope
from xblock.fragment import Fragment


template_engine = jinja2.Environment(loader=jinja2.PackageLoader('xb_field_test'))


class FieldTestXBlock(XBlock):
    """
    Implements the Field Test XBlock
    """

    ############################################################################################
    # Fields
    ############################################################################################

    # UserScope.NONE:
    settings_none_usage = fields.String(
        display_name="Settings - NONE|USAGE",
        #scope=Scope(UserScope.NONE, BlockScope.USAGE),
        scope=Scope.settings,  # Note that the line above doesn't work; apparently using the name is required
        default="settings_none_usage default",
    )
    content_none_definition = fields.String(
        display_name="Content - NONE|DEFINITION",
        #scope=Scope(UserScope.NONE, BlockScope.DEFINITION),
        scope=Scope.content,
        default="content_none_definition default",
    )
    # Unfortunately, even defining these fields will cause split to throw errors when attempting
    # to save any field at all, so it is not possible to even define them.
    #misc_none_type = fields.String(
    #    display_name="Misc - NONE|TYPE",
    #    scope=Scope(UserScope.NONE, BlockScope.TYPE),
    #    default="misc_none_type default",
    #)
    #misc_none_all = fields.String(
    #    display_name="Misc - NONE|ALL",
    #    scope=Scope(UserScope.NONE, BlockScope.ALL),
    #    default="misc_none_all default",
    #)

    # UserScope.ONE:
    user_state_one_usage = fields.String(
        display_name="User State - ONE|USAGE",
        #scope=Scope(UserScope.ONE, BlockScope.USAGE),
        scope=Scope.user_state,
        default="user_state_one_usage default",
    )
    #misc_one_definition = fields.String(
    #    display_name="Misc - ONE|DEFINITION",
    #    scope=Scope(UserScope.ONE, BlockScope.DEFINITION),
    #    default="misc_one_definition default",
    #)
    preferences_one_type = fields.String(
        display_name="Preferences - ONE|TYPE",
        #scope=Scope(UserScope.ONE, BlockScope.TYPE),
        scope=Scope.preferences,
        default="preferences_one_type default",
    )
    user_info_one_all = fields.String(
        display_name="Use Info - ONE|ALL",
        #scope=Scope(UserScope.ONE, BlockScope.ALL),
        scope=Scope.user_info,
        default="user_info_one_all default",
    )

    # UserScope.ALL:
    user_state_summary_all_usage = fields.String(
        display_name="User State Summary - ALL|USAGE",
        #scope=Scope(UserScope.ALL, BlockScope.USAGE),
        scope=Scope.user_state_summary,
        default="user_state_summary_all_usage default",
    )
    #misc_all_definition = fields.String(
    #    display_name="Misc - ALL|DEFINITION",
    #    scope=Scope(UserScope.ALL, BlockScope.DEFINITION),
    #    default="misc_all_definition default",
    #)
    #misc_all_type = fields.String(
    #    display_name="Misc - ALL|TYPE",
    #    scope=Scope(UserScope.ALL, BlockScope.TYPE),
    #    default="misc_all_type default",
    #)
    #misc_all_all = fields.String(
    #    display_name="Misc - ALL|ALL",
    #    scope=Scope(UserScope.ALL, BlockScope.ALL),
    #    default="misc_all_all default",
    #)

    @property
    def display_name_with_default(self):
        return u"Field Test XBlock"

    def get_field_info(self):
        """
        Get a list of all fields: each field's name, value, supported by the current runtime, etc.
        """
        for field in self.fields.values():

            if not hasattr(FieldTestXBlock, field.name) or hasattr(XBlock, field.name):
                continue  # Mixin/inherited field - ignore

            data = {"name": field.name}
            try:
                data["value"] = getattr(self, field.name)
            except InvalidScopeError:
                data["supported"] = False
            else:
                data["supported"] = True
                data["display_name"] = field.display_name
            yield data

    ############################################################################################
    # Views
    ############################################################################################

    def student_view(self, context):
        """
        The main view of this XBlock.
        """
        template = template_engine.get_template('student_view.html')
        html = template.render({
            "fields": list(self.get_field_info()),
        })
        fragment = Fragment(html)
        fragment.add_css_url(self.runtime.local_resource_url(self, 'public/style.css'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/client.js'))

        fragment.initialize_js('FieldTestXBlock', {})

        return fragment

    # For edx-platform, the Scope.content / Scope.settings fields can only be modified in a studio_view context:
    studio_view = student_view

    ############################################################################################
    # Client-side AJAX callback handlers
    ############################################################################################

    @XBlock.json_handler
    def update_field(self, data, suffix=''):
        """
        Update a field
        """
        field_name = data["field_name"]
        new_value = data["new_value"]

        # Save the new value:
        setattr(self, field_name, new_value)

    ############################################################################################
    # Misc
    ############################################################################################

    @staticmethod
    def workbench_scenarios():
        """
        An XML scenario for display in the XBlock SDK workbench.
        """
        return [
            ("FieldTestXBlock default scenario", "<field-test/>"),
        ]
