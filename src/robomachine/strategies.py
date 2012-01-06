#  Copyright 2011-2012 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class DepthFirstSearch(object):

    def __init__(self, machine, max_actions):
        self._machine = machine
        self._max_actions = max_actions

    def tests(self):
        for values in self._variable_value_sets(self._machine.variables):
            self._machine.apply_variable_values(values)
            for test in self._generate_all_from(self._machine.start_state, self._max_actions):
                yield test, values

    def _variable_value_sets(self, variables):
            if not variables:
                return ((),)
            return (vs for vs in self._var_set(variables) if self._machine.rules_are_ok(vs))

    def _var_set(self, vars):
        if not vars:
            return [[]]
        return ([val]+sub_set for val in vars[0].values for sub_set in self._var_set(vars[1:]))

    def _generate_all_from(self, state, max_actions):
        if not state.actions or max_actions == 0:
            yield []
        else:
            for action in state.actions:
                for test in self._generate_all_from(action.next_state, max_actions-1):
                    yield [action]+test