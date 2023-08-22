import {UserRole} from "../../user/user.ts";
import {RouteRecordRaw} from "vue-router";
import CarbonAuditPage from "./CarbonAuditPage.vue";
import CarbonAuditAddPage from "./add/CarbonAuditAddPage.vue";

const CARBON_AUDIT_ROUTES: RouteRecordRaw[] = [
    {
        name: 'CarbonAudit', path: '/carbon-audit', component: CarbonAuditPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.CARBON_AUDITOR],
            },
            navigationMenu: {type: 'entry', entry: {icon: 'co2', label: 'Carbon Audit'}}
        }
    },
    {
        name: 'CarbonAuditAdd', path: '/carbon-audit/add', component: CarbonAuditAddPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.CARBON_AUDITOR]
            },
            navigationMenu: {type: 'linked', routeName: 'CarbonAudit'}
        }
    }
];

export default CARBON_AUDIT_ROUTES