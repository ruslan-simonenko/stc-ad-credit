export interface CarbonAudit {
    id: number,
    business_id: number,
    score: number,
    report_date: Date,
    report_url: string,
}

export interface CarbonAuditAddFormDTO {
    business_id: number,
    score: number,
    report_date: Date,
    report_url: string,
}

export interface CarbonAudits {
    items: Array<CarbonAudit>,
    fetching: boolean,
    error: boolean,
}
