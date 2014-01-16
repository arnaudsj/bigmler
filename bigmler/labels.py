# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2013-2014 BigML
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Multi-label labels management functions

"""
MULTI_LABEL_LABEL = "multi-label label: "


def get_label_field(objective_name, label):
    """Returns a field name based on the original multi-label objective field
       name and the label

    """
    return "%s - %s" % (objective_name, label)


def label_model_args(name, label, all_labels, model_fields, objective_field):
    """Adapts model arguments to choose only one label field as objective

    """
    label_field = get_label_field(objective_field, label)
    # model_fields must be given in a relative syntax
    single_label_fields = model_fields[:]
    single_label_fields.extend(
        map(lambda x: ("-%s" % get_label_field(objective_field, x)
                       if x != label_field
                       else
                       "+%s" % get_label_field(objective_field,
                                               x)),
            all_labels))
    single_label_fields.append("-%s" % objective_field)
    new_name = "%s for %s" % (name, label_field)

    return new_name, label_field, single_label_fields


def get_multi_label_data(resource):
    """Returns the multi-label info from the resource

    """
    if ('object' in resource and 'user_metadata' in resource['object'] and
           'multi_label_data' in resource['object']['user_metadata']):
        return resource['object']['user_metadata']['multi_label_data']

def get_all_labels(multi_label_data):
    """Extracts the complete set of labels from the stored multi_label_data.

    """
    new_fields = multi_label_data['generated_fields']
    new_objective_fields= new_fields[str(multi_label_data['objective_column'])]
    return [new_field[0] for new_field in new_objective_fields]

def multi_label_sync(objective_field, labels, multi_label_data, fields):
    """Returns the right objective_field, labels, and all_labels info
       either from the user given values or from the structure stored
       in user_metadata

    """

    if objective_field is None:
        objective_field = multi_label_data['objective_name']
    if fields is not None:
        objective_id = fields.field_id(objective_field)
        objective_name = fields.field_name(objective_id)
        objective_column = fields.field_column_number(objective_id)
        multi_label_data['objective_name'] = objective_name
        multi_label_data['objective_column'] = objective_column
        multi_label_data['objective_id'] = objective_id

    # extract labels from the new fields [label, column] information
    all_labels = get_all_labels(multi_label_data)
    if not labels:
        labels = all_labels
    return (objective_field, labels, all_labels, multi_label_data)        
