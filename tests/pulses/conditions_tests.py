import unittest
from typing import Optional

from qctoolkit.pulses.instructions import InstructionPointer, Trigger, CJMPInstruction, GOTOInstruction
from qctoolkit.pulses.conditions import HardwareCondition, SoftwareCondition, ConditionEvaluationException

from tests.pulses.sequencing_dummies import DummySequencingElement, DummySequencer, DummyInstructionBlock


class HardwareConditionTest(unittest.TestCase):
    
    def test_build_sequence_loop(self) -> None:        
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        body = DummySequencingElement()
        
        trigger = Trigger()
        condition = HardwareCondition(trigger)
        condition.build_sequence_loop(delegator, body, sequencer, [], block)
        
        self.assertEqual(1, len(block.embedded_blocks))
        body_block = block.embedded_blocks[0]
        
        self.assertEqual([CJMPInstruction(trigger, body_block, 0)], block.instructions, "The expected conditional jump was not generated by HardwareConditon.")
        self.assertEqual(InstructionPointer(block, 0), body_block.return_ip, "The return address of the loop body block was set wrongly by HardwareCondition.")
        self.assertEqual({body_block: [(body, [])]}, sequencer.sequencing_stacks, "HardwareCondition did not correctly push the body element to the stack")
        self.assertFalse(condition.requires_stop())
    
    def test_build_sequence_branch(self) -> None:
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        if_branch = DummySequencingElement()
        else_branch = DummySequencingElement()
        
        trigger = Trigger()
        condition = HardwareCondition(trigger)
        condition.build_sequence_branch(delegator, if_branch, else_branch, sequencer, [], block)
        
        self.assertEqual(2, len(block.embedded_blocks))
        if_block = block.embedded_blocks[0]
        else_block = block.embedded_blocks[1]
        
        self.assertEqual([CJMPInstruction(trigger, if_block, 0), GOTOInstruction(else_block, 0)], block.instructions, "The expected jump instruction were not generated by HardwareConditon.")
        self.assertEqual(InstructionPointer(block, 2), if_block.return_ip, "The return address of the if branch block was set wrongly by HardwareConditon.")
        self.assertEqual(InstructionPointer(block, 2), else_block.return_ip, "The return address of the else branch block was set wrongly by HardwareConditon.")
        self.assertEqual({if_block: [(if_branch, [])], else_block: [(else_branch, [])]}, sequencer.sequencing_stacks, "HardwareCondition did not correctly push the branch elements to the stack")
        

class IterationCallbackDummy:
    
    def __init__(self, callback_return: Optional[bool]) -> None:
        super().__init__()
        self.callback_return = callback_return
        self.loop_iteration = 0
    
    def callback(self, loop_iteration: int) -> Optional[bool]:
        self.loop_iteration = loop_iteration
        return self.callback_return
        

class SoftwareConditionTest(unittest.TestCase):
    
    def test_build_cannot_evaluate(self) -> None:
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        body = DummySequencingElement()
        
        condition = SoftwareCondition(lambda loop_iteration: None)
        
        self.assertTrue(condition.requires_stop())
        self.assertRaises(ConditionEvaluationException, condition.build_sequence_loop, delegator, body, sequencer, [], block)
        self.assertRaises(ConditionEvaluationException, condition.build_sequence_branch, delegator, body, body, sequencer, [], block)
        self.assertEqual(str(ConditionEvaluationException()), "The Condition can currently not be evaluated.")
        
    def test_build_sequence_loop_true(self) -> None:
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        body = DummySequencingElement()
        callback = IterationCallbackDummy(True)
        
        condition = SoftwareCondition(lambda loop_iteration: callback.callback(loop_iteration))
        condition.build_sequence_loop(delegator, body, sequencer, [], block)
        
        self.assertEqual(0, callback.loop_iteration)
        self.assertFalse(block.instructions)
        self.assertEqual({block: [(delegator, []), (body, [])]}, sequencer.sequencing_stacks)
        
        condition.build_sequence_loop(delegator, body, sequencer, [], block)
        self.assertEqual(1, callback.loop_iteration)
        
    def test_build_sequence_loop_false(self):
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        body = DummySequencingElement()
        callback = IterationCallbackDummy(False)
        
        condition = SoftwareCondition(lambda loop_iteration: callback.callback(loop_iteration))
        condition.build_sequence_loop(delegator, body, sequencer, [],  block)
        
        self.assertEqual(0, callback.loop_iteration)
        self.assertFalse(block.instructions)
        self.assertFalse(sequencer.sequencing_stacks)
        
        condition.build_sequence_loop(delegator, body, sequencer, [], block)
        self.assertEqual(0, callback.loop_iteration)
        
    def test_build_sequence_branch_true(self):
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        if_branch = DummySequencingElement()
        else_branch = DummySequencingElement()
        callback = IterationCallbackDummy(True)
        
        condition = SoftwareCondition(lambda loop_iteration: callback.callback(loop_iteration))
        condition.build_sequence_branch(delegator, if_branch, else_branch, sequencer, [], block)
        
        self.assertEqual(0, callback.loop_iteration)
        self.assertFalse(block.instructions)
        self.assertEqual({block: [(if_branch, [])]}, sequencer.sequencing_stacks)
        
        condition.build_sequence_branch(delegator, if_branch, else_branch, sequencer, [], block)
        self.assertEqual(0, callback.loop_iteration)
        
        
    def test_build_sequence_branch_false(self):
        sequencer = DummySequencer()
        block = DummyInstructionBlock()
        
        delegator = DummySequencingElement()
        if_branch = DummySequencingElement()
        else_branch = DummySequencingElement()
        callback = IterationCallbackDummy(False)
        
        condition = SoftwareCondition(lambda loop_iteration: callback.callback(loop_iteration))
        condition.build_sequence_branch(delegator, if_branch, else_branch, sequencer, [], block)
        
        self.assertEqual(0, callback.loop_iteration)
        self.assertFalse(block.instructions)
        self.assertEqual({block: [(else_branch, [],)]}, sequencer.sequencing_stacks)
        
        condition.build_sequence_branch(delegator, if_branch, else_branch, sequencer, [], block)
        self.assertEqual(0, callback.loop_iteration)

if __name__ == "__main__":
    unittest.main(verbosity=2)