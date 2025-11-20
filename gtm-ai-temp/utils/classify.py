from typing import Literal

# VERY SIMPLE keyword rules to classify companies by role in construction.
# In a real system you'd enrich via LinkedIn/Crunchbase APIs, but keywords work well as a baseline.
def classify_company(name: str, title: str='') -> Literal['Builder','Owner','Partner','Competitor','Other']:
    n = (name or '').lower()
    t = (title or '').lower()
    # Known competitors to DroneDeploy (drone mapping/photogrammetry/field mgmt)
    competitors = [
        'pix4d','propeller','3dr','reconstruct','delair','skydio','hovermap','esri',
        'site scan','autodesk construction cloud','autodesk construction solutions',
        'bentley systems','contextcapture','openroads','navisworks','trimble',
        'procore','bluebeam','openspace','cupix','matterport','innovyze','nearview'
    ]
    partners = ['system integrator','consulting','consultancy','reseller','partner','si ',
                'channel','implementation','it services']
    builders = ['contractor','construct','build','gc','builder','engineering','engineers','design & build','civil','mep','aec']
    owners = ['owner','airport','authority','council','university','nhs','estate','developer','housing','rail','highways','water','utility','transport for','network rail','heathrow','hs2']
    if any(k in n for k in competitors) or any(k in t for k in competitors):
        return 'Competitor'
    if any(p in t for p in partners):
        return 'Partner'
    if any(k in n for k in builders) or any(k in t for k in builders):
        return 'Builder'
    if any(k in n for k in owners) or any(k in t for k in owners):
        return 'Owner'
    return 'Other'
