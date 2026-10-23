"""Exercise Vitrine menu integration independently of native download readiness."""
from pathlib import Path
import json,plistlib,shutil,subprocess,time,sys
root=Path(__file__).resolve().parents[1]
out=root/'build/vitrine-ui-deb';app=out/'PixieVitrineFixture.app';app.mkdir(parents=True,exist_ok=True)
def run(*args,check=True):
    result=subprocess.run(list(map(str,args)),cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
    if check and result.returncode:raise RuntimeError(result.stdout)
    return result.stdout.strip()
devices=json.loads(run('xcrun','simctl','list','devices','--json'))['devices']
udid=next((d['udid'] for group in devices.values() for d in group if d['state']=='Booted' and 'iPhone' in d['name'] and d.get('isAvailable')),None)
sdk=run('xcrun','--sdk','iphonesimulator','--show-sdk-path')
sources=['src/DownloadSettingsUI.m','src/Diagnostics.m','src/DiagnosticTrace.m','src/NativeKeyTrace.m','src/WireProto.m','src/Localization.m','tests/trace_platform_stub.m','tests/SettingsFixtureActions.m','tests/VitrineSettingsFixture.m']
run('xcrun','clang','-target','arm64-apple-ios27.0-simulator','-isysroot',sdk,'-fobjc-arc','-std=gnu11','-Isrc','-DSAP_UI_FIXTURE','-DSAP_VITRINE_FIXTURE',*sources,'-framework','UIKit','-framework','Foundation','-framework','CoreGraphics','-Wl,-export_dynamic','-o',app/'PixieVitrineFixture')
bundle='local.pixie.vitrine-deb-fixture'
(app/'Info.plist').write_bytes(plistlib.dumps({'CFBundleIdentifier':bundle,'CFBundleExecutable':'PixieVitrineFixture','CFBundleVersion':'1','CFBundleShortVersionString':'1','CFBundlePackageType':'APPL','LSRequiresIPhoneOS':True,'UIDeviceFamily':[1],'UILaunchScreen':{},'UIApplicationSceneManifest':{'UIApplicationSupportsMultipleScenes':False,'UISceneConfigurations':{'UIWindowSceneSessionRoleApplication':[{'UISceneConfigurationName':'Default','UISceneDelegateClassName':'VitrineFixtureScene'}]}}}))
run('codesign','--force','--sign','-','--timestamp=none',app)
if not udid or '--build-only' in sys.argv:
    print('PASS: Vitrine settings fixture compiled; simulator execution skipped (no booted iPhone simulator or build-only)')
    sys.exit(0)
run('xcrun','simctl','install',udid,app)
for scenario in ['supported','unsupported']:
    run('xcrun','simctl','terminate',udid,bundle,check=False)
    folder=Path(run('xcrun','simctl','get_app_container',udid,bundle,'data'))/'Documents';result=folder/'result.log';result.unlink(missing_ok=True)
    run('xcrun','simctl','launch',udid,bundle,*(['--unsupported'] if scenario=='unsupported' else []))
    until=time.monotonic()+12
    while time.monotonic()<until:
        if result.exists():break
        time.sleep(.25)
    assert result.exists(),f'{scenario}: fixture did not complete'
    target=out/scenario;target.mkdir(exist_ok=True)
    for name in ['result.log','vitrine-pixie.png']:shutil.copy2(folder/name,target/name)
    print(scenario,result.read_text().strip(),flush=True)
