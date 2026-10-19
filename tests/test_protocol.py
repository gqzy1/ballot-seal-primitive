import json
from pathlib import Path
import pytest
from gltest.direct import VMContext, deploy_contract

SOURCE = Path(__file__).parents[1] / 'contracts/ballot_seal.py'
TEXT = 'Pay the design guild 1000 USDC to produce one logo by 1 December 2026. No admin permissions.'

@pytest.fixture
def env():
    vm = VMContext()
    with vm.activate():
        c = deploy_contract(SOURCE, vm, sdk_version='v0.2.16')
        yield vm, c

def labels(**kw):
    return {k: {'label': kw.get(k, 'SAME'), 'reason': 'The specified terms are compared in this dimension.',
                'before_quote': 'Pay', 'after_quote': 'Pay'}
            for k in ['budget','beneficiary','scope','deadline','authority']}

def mock(vm, **kw):
    vm.mock_llm('.*', json.dumps(labels(**kw)))

def test_epoch_and_immutable_history(env):
    vm,c = env
    ref = c.create('logo','Logo grant',TEXT)
    c.acknowledge(ref,1)
    mock(vm)
    c.revise('logo',1,TEXT+' ')
    assert json.loads(c.get_acknowledgement(ref,str(vm.sender)))['applicable']
    assert json.loads(c.get_version(ref,1))['text'] == TEXT
    import hashlib
    assert json.loads(c.get_version(ref,1))['digest'] == hashlib.sha256(TEXT.encode()).hexdigest()
    vm._llm_mocks.clear()
    mock(vm,budget='CHANGED')
    c.revise('logo',2,TEXT.replace('1000','2000'))
    assert not json.loads(c.get_acknowledgement(ref,str(vm.sender)))['applicable']
    vm._llm_mocks.clear()
    mock(vm)
    c.revise('logo',3,TEXT.replace('1000','2000')+' ')
    assert not json.loads(c.get_acknowledgement(ref,str(vm.sender)))['applicable']
    c.acknowledge(ref,4)
    assert json.loads(c.get_acknowledgement(ref,str(vm.sender)))['exact_current_version']

@pytest.mark.parametrize('dim',['budget','beneficiary','scope','deadline','authority'])
@pytest.mark.parametrize('verdict',['CHANGED','UNCERTAIN'])
def test_any_dimension_invalidates(env,dim,verdict):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    c.acknowledge(ref,1)
    mock(vm,**{dim:verdict})
    c.revise('p',1,TEXT+' Updated.')
    p=json.loads(c.get_proposal(ref))
    assert p['epoch']==2
    assert not json.loads(c.get_acknowledgement(ref,str(vm.sender)))['applicable']
    assert p['current']['action']==('RECONFIRM' if verdict=='CHANGED' else 'REVIEW')

def test_stale_duplicate_and_nochange(env):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    for call in [lambda:c.create('p','Grant',TEXT),lambda:c.revise('p',0,TEXT+'x'),lambda:c.revise('p',1,TEXT),lambda:c.acknowledge(ref,2)]:
        with pytest.raises(Exception):call()
    assert json.loads(c.get_proposal(ref))['head']==1

@pytest.mark.parametrize('bad',[{}, {'budget':'SAME'}, dict(labels(),extra='SAME'),labels(budget=True),labels(scope='OK')])
def test_malformed_rejected(env,bad):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    vm.mock_llm('.*',json.dumps(bad))
    with pytest.raises(Exception):c.revise('p',1,TEXT+'x')
    assert json.loads(c.get_proposal(ref))['head']==1

def test_independent_validator(env):
    vm,c=env
    c.create('p','Grant',TEXT)
    mock(vm,budget='CHANGED')
    c.revise('p',1,TEXT+'x')
    validator=vm._captured_validators[-1][2]
    from genlayer import gl
    assert validator(gl.vm.Return(labels(budget='CHANGED')))
    assert not validator(gl.vm.Return(labels(scope='CHANGED')))
    assert not validator(gl.vm.Return({'budget':'CHANGED'}))

def test_owner_isolation_and_acknowledger_isolation(env):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    from genlayer import Address
    original=vm.sender
    with vm.prank(Address('0x'+'b'*40)):
        with pytest.raises(Exception):c.revise('p',1,TEXT+'x')
        second=c.create('p','Other grant',TEXT)
        c.acknowledge(ref,1)
        assert second!=ref
    assert not json.loads(c.get_acknowledgement(ref,str(original)))['applicable']

@pytest.mark.parametrize('text',['','x'*19,'x'*6001])
def test_input_bounds(env,text):
    vm,c=env
    with pytest.raises(Exception):c.create('p','Grant',text)

def test_ack_history_is_immutable(env):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    c.acknowledge(ref,1)
    old=json.loads(c.get_acknowledgement_history(ref,str(vm.sender)))
    mock(vm,budget='CHANGED')
    c.revise('p',1,TEXT+' More terms.')
    c.acknowledge(ref,2)
    new=json.loads(c.get_acknowledgement_history(ref,str(vm.sender)))
    assert len(new)==2 and new[0]==old[0]
    assert new[1]['epoch']==2
    with pytest.raises(Exception):c.acknowledge(ref,2)
    assert json.loads(c.get_acknowledgement_history(ref,str(vm.sender)))==new

def test_parent_digests_and_unicode(env):
    vm,c=env
    original=TEXT+' 设计工作室 🌐\n'
    ref=c.create('p','Grant',original)
    mock(vm)
    c.revise('p',1,original+' ')
    v1=json.loads(c.get_version(ref,1));v2=json.loads(c.get_version(ref,2))
    import hashlib
    assert v1['digest']==hashlib.sha256(original.encode()).hexdigest()
    assert v2['parent_digest']==v1['digest']
    assert v2['assessment']['budget']['reason']

def test_exact_text_bounds_including_whitespace(env):
    _,c=env
    with pytest.raises(Exception):c.create('p','Grant',' '*6000+TEXT)
    with pytest.raises(Exception):c.create('p',' '*100+'T',TEXT)

def test_absent_or_fabricated_reason_rejected(env):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    invalid=labels();invalid['budget']['after_quote']='a quote that is not in the document'
    vm.mock_llm('.*',json.dumps(invalid))
    with pytest.raises(Exception):c.revise('p',1,TEXT+'x')
    assert json.loads(c.get_proposal(ref))['head']==1

def test_limits_and_non_resurrection(env):
    vm,c=env
    ref=c.create('p','Grant',TEXT)
    mock(vm)
    for v in range(1,32):c.revise('p',v,TEXT+' '*v)
    with pytest.raises(Exception):c.revise('p',32,TEXT+'x')
    for i in range(15):c.create('p'+str(i),'Grant',TEXT)
    with pytest.raises(Exception):c.create('overflow','Grant',TEXT)

def test_same_action_different_dimension_rejected(env):
    vm,c=env
    c.create('p','Grant',TEXT)
    mock(vm,budget='CHANGED');c.revise('p',1,TEXT+'x')
    from genlayer import gl
    validate=vm._captured_validators[-1][2]
    assert not validate(gl.vm.Return(labels(authority='CHANGED')))
    equivalent=labels(budget='CHANGED');equivalent['budget']['reason']='A different wording explains the same independently agreed classification.'
    assert validate(gl.vm.Return(equivalent))
